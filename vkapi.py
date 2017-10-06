import vk
import urllib
import os
from multiprocessing import Pool
from progress.bar import Bar
from functools import partial

app_id = '6124903'


def auth(app_id, login, password, scope="photos"):
    session = vk.AuthSession(app_id, login, password, scope=scope)
    return session


def cycles_number(owner_id):
    albums = vk_api.photos.getAlbums(owner_id=owner_id, need_system=1)
    album_saved_size = albums[2]['size']
    number_of_cycles = round(album_saved_size/1000.0)
    print ("There are %i images.") % album_saved_size
    return number_of_cycles


def collect_URL(owner_id, cycle, offset):
    url_list = []
    for i in range(0, int(cycle + 1)):
        # count = 1000, offset = offset + 1000 * i
        photos = vk_api.photos.get(owner_id=owner_id, album_id="saved", rev=0,
                                   photo_sizes=1, count=1000, offset=offset+1000*i)
        for photo in photos:
            url = photo['sizes'][-1]['src']
            url_list.append(url)

    return url_list


def download_images(url, folder):
    break_url = url.split('/')
    id_photo = break_url[-1]
    urllib.urlretrieve(url, os.path.join(os.getcwd(),
                                         folder + id_photo))


def choose_folder():
    folder_name = raw_input("Choose a name for the folder > ")
    if not (os.path.isdir(folder_name)):
        os.makedirs(folder_name)
        number_of_files = 0
    else:
        number_of_files = len([name for name in os.listdir(folder_name) if os.path.isfile(name)])
        print "The folder already exists. There are %i images." % (number_of_files)
    return folder_name, number_of_files


if __name__ == '__main__':
    login = raw_input('Insert your vk login > ')
    password = raw_input('Insert your vk password > ')
    vk_api = vk.API(auth(app_id, login, password))

    folder_name, offset = choose_folder()
    owner_id = raw_input('Owner ID > ')
    cycles = cycles_number(owner_id)
    url_list = collect_URL(owner_id, cycles, offset)

    print "Downloading %i images to %s folder." % (len(url_list), folder_name)
    pool = Pool()
    bar = Bar('Processing', max=len(url_list))
    for i in pool.imap(partial(download_images, folder = "Christina's Saved Images/"), url_list):
        bar.next()
    bar.finish()
