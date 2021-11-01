from os import walk, path, stat
import pandas as pd
import math
import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"


folder = r"F:\Games"

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

result = [path.join(dp, f) for dp, dn, filenames in walk(folder) for f in filenames]
result_with_size = [(x, stat(x).st_size ) for x in result]
result_with_parent = [{"file_path": y[0], "size": y[1], "parent_folder": path.dirname(y[0])} for y in result_with_size]

df = pd.DataFrame(result_with_parent)
size_by_folder = df.groupby(['parent_folder'], as_index=False)['size'].sum()
size_by_folder = size_by_folder.sort_values(by=['size'], ascending=False)

size_by_folder['size'] = size_by_folder['size'].apply(convert_size)
size_by_folder.reset_index(drop=True, inplace=True)
size_by_folder.to_csv("size_by_folder.csv")

fig = go.Figure(data=[go.Table(
    header=dict(values=list(size_by_folder.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[size_by_folder.parent_folder, size_by_folder.size],
               fill_color='lavender',
               align='center'))
])

fig.show()

breakpoint = None