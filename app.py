from dash import html, dcc
from processing import process_image
from dotenv import load_dotenv
from utils.callbacks import callback_display_selected_data, callback_display_image_on_hover, update_interaction_mode, \
    clientside_callback

import os
import dash
import dash_bootstrap_components as dbc
import plotly.express as px


load_dotenv()

TEXT_1 = """
Many students get frightened the first time they encounter k-space. An MRI scanner doesn’t “see” body structures \
directly — it collects signals as frequencies from proton spins, stored as pixels in a coordinate grid. At first it \
looks random, but this project is a distilled visualization of how those abstract pixels (amplitude, phase, spatial \
frequency) combine to form the final image.

🎯 **Goal.**
Although many k-space exploration tools exist, they don't offer a clear intuition for how these “pixels” \
translate into the final image. This minimal visualization is designed for a clean, focused understanding of \
how each k-space point (a spatial frequency component, or "wave") — or groups of them — contributes to the \
reconstructed image.
"""

TEXT_2 = """
✍️ **Note.**
A single k-space pixel does not correspond to a single pixel in the final MRI image. Instead, each k-space point \
corresponds to all the pixels in the image by encoding information about:
+ Amplitude → how strongly it contributes to the image (intensity).
+ Phase → how the wave pattern is shifted in k-space.
+ Spatial frequency → the repeating “bar” pattern it represents, which becomes visible when hovering over pixels in \
the demo below.
"""

TEXT_markdown = """
**Visual demonstration.** Interact with the demo above: hover over any pixel to reveal its spatial frequency and phase.\
 Select multiple pixels to see their patterns add up — each one contributing to the image. The larger the area you \
 select, the closer the sum comes to reconstructing the original image.
"""


images, imgs, idx_mat, idx_mat_shifted, grid_data = process_image('assets/images/brain.jpg')

external_scripts = [
    "https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"
]

app = dash.Dash(external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "k-space"
server = app.server

fig = px.imshow(grid_data,
                labels=dict(x="Frequency", y="Phase", color="Magnitude"),
                color_continuous_scale='gray',
                # title='k-space (aka Fourier space)',
                )
fig.update_layout(
    margin=dict(t=20, l=20, r=20, b=10),
    xaxis_visible=True,
    yaxis_visible=True,
    hovermode="closest",
    dragmode="select",
    newselection=dict(line=dict(color='white', width=2)),
    activeselection=dict(fillcolor='white', opacity=.3),
    barcornerradius=5,
    coloraxis_showscale=False,

)
fig.update_traces(hoverinfo="none", hovertemplate=None)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)

app.layout = html.Div(
    [
        html.H1("MRI to K-Space. K-Space to Image.", style={
            'fontFamily': 'Inter, medium',
            'fontSize': '32px',
            'textAlign': 'center',
            'marginTop': '50px'
        }),
        dbc.Row(
                [
                    dbc.Col([html.P(dcc.Markdown(TEXT_1), className="column"), html.Div(
                        html.Figure
                            ([html.Img(
                                src="assets/images/scheme.png",
                                style={"width": "40%"}),
                            html.Figcaption(dcc.Markdown("**Figure 1.** Stacking wave patterns."))
                        ]),
                        style={"textAlign": "center", 'textJustify': 'inter-character'}   # centers the image
                             )]),
                    dbc.Col(
                        [
                            html.P(dcc.Markdown(TEXT_2), className="column"),
                            html.Center(
                                html.Div(dbc.Button(children="Skip to Demo...",
                                                    className="btn btn-skip",
                                                    n_clicks=0,
                                                    href='#section-demo',
                                                    external_link=True
                                                    ),
                                         style={'width': 200})
                            )
                        ]
                    ),
                ]
            ),
        html.Br(),
        html.Hr(),
        html.H1("From Fourier Space to Image",
                id='section-demo',
                style={
                    'fontFamily': 'Inter, medium',  # or your preferred font
                    'fontSize': '26px',
                    'textAlign': 'center',
                    'marginTop': '50px',
                }),
        html.Div(className='container',
                 children=[
                     dcc.Graph(
                         id='heatmap',
                         figure=fig,
                         clear_on_unhover=True,
                         style={'width': '50%', 'display': 'block',
                                },
                         config={'modeBarButtonsToAdd': ['select2d', 'lasso2d']},
                     ),
                     dcc.Tooltip(id='heatmap-tooltip', show=True),
                     html.Img(id='selected-image', style={'width': '20%',
                                                          'display': 'block',
                                                          'borderRadius': '10px',
                                                          }),
                     html.Div(html.Img(id='hover-image', style={'width': '12%',
                                          'borderRadius': '10px',
                                          'border': '4px solid black',
                                          'top': '0',
                                          'left': '0',
                                          'position': 'absolute',
                                          'pointerEvents': 'none'
                                                                })),
                 ],
                 style={
                        "display": "flex",
                        "justifyContent": "center",  # center horizontally
                        "alignItems": "center",      # align vertically
                        "gap": "50px",               # space between graph and image
                        "position": "relative",
                        'fontFamily': 'Inter, regular'
                 }
                 ),
        dcc.Markdown(TEXT_markdown),
        dcc.Markdown("If you liked the visualization idea, you can:"),
        dbc.Button(children=html.Img(src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png",
                                     style={
                                         "width": "175px",
                                              }),
                   href=os.getenv("BMC_URL"),
                   target="_blank",
                   # className="btn btn.btn-buy",
                   style={"background-color": "transparent",
                          "padding": "0px",
                          "border-color": "black",
                          "border-radius": "8px"
                          }
                   ),
        html.Div(style={"height": "25px"}),
        dcc.Store(id='interaction-mode', data='hover'),
        dcc.Store(id="hover-reset")
    ],
    style={"maxWidth": "1000px", "margin": "0 auto"}
)

callback_display_selected_data(idx_mat_shifted, images)
callback_display_image_on_hover(idx_mat, imgs)


if __name__ == '__main__':
    app.run(debug=False)
