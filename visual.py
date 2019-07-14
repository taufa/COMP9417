
import matplotlib.pyplot as plt
import gmplot
import os
from main import NYC_LONG, NYC_LAT, MARGIN, N_ROWS
from preprocess import clean_data

dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory
df = clean_data()

def plot_pickups(df):
    plt.plot(list(df.pickup_longitude), list(df.pickup_latitude), '.', markersize=0.5)
    plt.title('Pickups')
    plt.xlabel('Longitudes')
    plt.ylabel('Latitudes')
    plt.savefig(f'images/{N_ROWS}_pickups.png')
    plt.clf() # clears the buffer so figures dont overlap
    #plt.show()

def plot_dropoffs(df):
    plt.plot(list(df.dropoff_longitude), list(df.dropoff_latitude), '.', markersize=0.5)
    plt.title('Dropoffs')
    plt.xlabel('Longitudes')
    plt.ylabel('Latitudes')
    plt.savefig(f'images/{N_ROWS}_dropoffs.png')
    plt.clf() # clears the buffer so figures dont overlap
    #plt.show()
    
def create_scatter_map(lat_list, long_list, color, filename):
    gmap = gmplot.GoogleMapPlotter(NYC_LAT, NYC_LONG, 11)
    gmap.apikey = 'AIzaSyCCqayBxqLtARcShlcms6ZQiqspIM0_Lxc'
    gmap.scatter(lat_list, long_list, color, size=40, marker=False ) 
    gmap.draw(f'{dir_path}\\images\\{filename}.html')

def create_heat_map(lat_list, long_list, filename):
    gmap = gmplot.GoogleMapPlotter.from_geocode("New York City")
    gmap.apikey = 'AIzaSyCCqayBxqLtARcShlcms6ZQiqspIM0_Lxc'
    gmap.heatmap(lat_list, long_list)
    gmap.draw(f'{dir_path}\\images\\{filename}.html')


'''
NOTE: This creates a scatter map from google map api. It will be very slow to plot >50000 data points
and will generate a very large plot file. Uncomment if you want to try just make sure to use a smaller
dataset first to test. All plots are saved in images folder (html format)
'''
##create_scatter_map(list(df.pickup_latitude), list(df.pickup_longitude), '#FF0000', 'pickup_scatter_map')
##create_scatter_map(list(df.dropoff_latitude), list(df.dropoff_longitude), '#0000FF', 'dropoff_scatter_map')

plot_dropoffs(df)
plot_pickups(df)
