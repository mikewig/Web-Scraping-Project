import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def createCharts(df):

    fig, ax = plt.subplots(figsize=(10,6))

    for i, row in df.iterrows():
        ax.plot([0, 1], [row['price'], row['price']], label=row['name'])

        ax.set_title('Price of the popular cryptos')
        ax.set_xlabel('Índice')
        ax.set_ylabel('Price in USD')
        ax.legend(loc='upper left')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        return buf