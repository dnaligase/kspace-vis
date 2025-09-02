from dash import html, dcc, Input, Output
from processing import process_image
from utils.callbacks import callback_display_selected_data, callback_display_image_on_hover, update_interaction_mode, \
    clientside_callback

import dash
import dash_bootstrap_components as dbc
import plotly.express as px


TEXT = "<br>Theory.</br>Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
       "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a " \
       "galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but " \
       "also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s " \
       "with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop " \
       "publishing software like Aldus PageMaker including versions of Lorem Ipsum."

TEXT_markdown = """
**Visual demonstration.** Interact with visualization demo above. Hover over each pixel to display its respective
spatial frequency and phase. Select the set of pixels to see their sum; see how their sum results in image formation by 
simply adding spatial patterns together. The more area you cover with selection tool, the more you reconstruct the 
original image.
"""


images, imgs, idx_mat, idx_mat_shifted, grid_data = process_image('assets/images/brain.jpg')

external_scripts = [
    "https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"
]

app = dash.Dash(external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

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
    newselection=dict(line=dict(color='white')),
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
            'fontFamily': 'Arial, medium',  # or your preferred font
            'fontSize': '32px',
            'textAlign': 'center',
            'marginTop': '50px'
        }),
        dbc.Row(
                [
                    dbc.Col([html.P(TEXT), html.Div(
                        html.Img(
                            src="assets/images/scheme.png",
                            style={"width": "40%"}),
                        style={"textAlign": "center"}   # centers the image
                             )]),
                    dbc.Col(
                        [
                            html.P(TEXT),
                            html.Div(dbc.Button(children="Skip to Demo...",
                                                style={"position": "relative"},
                                                className="btn btn-skip",
                                                n_clicks=0,
                                                href='#section-demo',
                                                external_link=True
                                                ),
                                     style={'width': 150})
                        ]
                    ),
                ]
            ),
        html.Br(),
        html.Hr(),
        html.H1("From Fourier Space to Image.",
                id='section-demo',
                style={
                    'fontFamily': 'Arial, medium',  # or your preferred font
                    'fontSize': '26px',
                    'textAlign': 'center',
                    'marginTop': '50px'
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
                     html.Div(html.Img(id='hover-image', style={'width': '8%',
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
                        # "overflow": "hidden",
                 }
                 ),
        dcc.Markdown(TEXT_markdown),

        dcc.Store(id='interaction-mode', data='hover'),
        dcc.Store(id="hover-reset")
    ],
    style={"maxWidth": "1000px", "margin": "0 auto"}
)

callback_display_selected_data(idx_mat_shifted, images)
callback_display_image_on_hover(idx_mat, imgs)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8931)
