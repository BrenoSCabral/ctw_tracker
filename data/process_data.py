import pandas as pd
import filt_data as filt


def process_data(data):
    df = data.dropna(subset=['ssh']).copy()
    dt = df.index.to_series().diff().median()  # intervalo típico (ex: 1 hora)
    groups = (df.index.to_series().diff() > dt * 1.5).cumsum()  # novo grupo se gap > 1.5*dt
    segments = [segment for _, segment in df.groupby(groups)]

    processed_segments = []

    for seg in segments:
        if len(seg) > 24 * 45:  # ignora segmentos inferiores a 1 mes
            seg = seg.copy()
            seg = filt.filter_data(seg)
            processed_segments.append(seg)


    return processed_segments


