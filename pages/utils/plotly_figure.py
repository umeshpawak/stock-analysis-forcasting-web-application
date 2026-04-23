import plotly.graph_objects as go

def plotly_table(df, height=300):
    """
    Creates a styled Plotly table from a pandas DataFrame 
    with bold headers and alternating row colors (light blue/gray).
    """
    # Make index a column if it has a meaningful name
    if df.index.name is not None:
        df = df.reset_index()
        
    # Formatting datetime columns purely for display
    for col in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetime64[ns]', 'datetime64']).columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')

    header_vals = [f"<b>{c}</b>" for c in df.columns]
    cell_vals = [df[col] for col in df.columns]
    
    # Colors
    header_color = '#d0e3f0'  # noticeable light blue for header
    row_odd_color = '#e4edf5' # very soft blue
    row_even_color = '#f2f6f9' # very light gray
    
    num_rows = len(df)
    row_colors = [row_odd_color if i % 2 == 0 else row_even_color for i in range(num_rows)]
    fill_colors = [row_colors] * len(df.columns)

    fig = go.Figure(data=[go.Table(
        header=dict(values=header_vals,
                    fill_color=header_color,
                    font=dict(size=14, color='black'),
                    align='left',
                    height=35),
        cells=dict(values=cell_vals,
                   fill_color=fill_colors,
                   font=dict(size=13, color='black'),
                   align='left',
                   height=30))
    ])
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=0, b=0))
    return fig
