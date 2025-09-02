import io
import base64
import numpy as np

from dash import Input, Output, callback, clientside_callback
from PIL import Image
from .utils import encode_array_to_base64


# display selected data
def callback_display_selected_data(idx_mat_shifted, images):
    @callback(
        Output('selected-image', 'src'),
        Input('heatmap', 'selectedData'),
    )
    def display_selected_data(selected_data):
        if selected_data is None:
            return "assets/images/placeholder.png"
        points = selected_data['range']
        xs = list(map(int, points['x']))
        ys = list(map(int, points['y']))
        idx_chunk = idx_mat_shifted[min(ys):max(ys), min(xs):max(xs)]

        images_chunk = images[:, :, idx_chunk.flatten()]
        chunk = images_chunk.sum(axis=-1)

        # TODO: separate into function
        res = (chunk - chunk.min(axis=(0, 1))) / (chunk.max(axis=(0, 1)) - chunk.min(axis=(0, 1)))
        res = res * (255 - 0) + 0

        img = res.astype(np.uint8)
        pil_img = Image.fromarray(img).resize((200, 200))
        buf = io.BytesIO()
        pil_img.save(buf, format='PNG')
        img_data = base64.b64encode(buf.getvalue()).decode()

        return f"data:image/png;base64,{img_data}"


@callback(
    Output('interaction-mode', 'data'),
    Input('heatmap', 'relayoutData')
)
def update_interaction_mode(relayout_data):
    if relayout_data is None:
        return 'hover'
    # Detect when selection is happening
    keys = relayout_data.keys()
    if any(k.startswith('xaxis.range') or k.startswith('yaxis.range') for k in keys):
        return 'selecting'
    return 'hover'


def callback_display_image_on_hover(idx_mat, imgs):
    @callback(
        Output('hover-image', 'src'),
        Input('heatmap', 'hoverData'),
        Input('interaction-mode', 'data'),
    )
    def display_image_on_hover(hover_data, mode):
        if mode != 'hover' or not hover_data:
            return None
        point = hover_data['points'][0]
        i = point['y']
        j = point['x']
        idx = idx_mat[i, j]
        return encode_array_to_base64(imgs[:, :, idx])


clientside_callback(
    """
    function(n, data) {
        return "";
    }
    """,
    Output("hover-image", "src", allow_duplicate=True),
    Input("hover-reset", "data"),
    prevent_initial_call=True
)
