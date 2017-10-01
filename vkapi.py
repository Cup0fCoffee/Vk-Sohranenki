import vk
import urllib
import os

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


def collect_URL(owner_id, cycle):
    url_list = []
    for i in range(0, int(cycle + 1)):
        # count = 1000, offset = 1000 * i
        photos = vk_api.photos.get(owner_id=owner_id, album_id="saved", rev=0,
                                   photo_sizes=1, count=1000, offset=1000*i)
        for photo in photos:
            url = photo['sizes'][-1]['src']
            url_list.append(url)

    return url_list


def download_images(url_list, folder):
    print "Downloading %i images to %s folder." % (len(url_list), folder)
    directory = folder+'/'
    img_downloaded = 0
    for url in url_list:
        break_url = url.split('/')
        id_photo = break_url[-1]
        urllib.urlretrieve(url, os.path.join(os.getcwd(),
                                             directory + id_photo))
        img_downloaded += 1
        show_progress(url_list, img_downloaded)


def choose_folder():
    folder_name = raw_input("Choose a name for the folder > ")
    if not (os.path.isdir(folder_name)):
        os.makedirs(folder_name)

    owner_id = raw_input('Owner ID: ')
    download_images(collect_URL(owner_id, cycles_number(owner_id)), folder_name)


def show_progress(url_list, img_downloaded):
    percentage = round(img_downloaded * 100 / len(url_list), 2)
    print ("\rDownloaded %i out of %i (%d%%)." % (img_downloaded, len(url_list),
                                                  percentage))


if __name__ == '__main__':
    login = raw_input('Insert your vk login > ')
    password = raw_input('Insert your vk password > ')
    vk_api = vk.API(auth(app_id, login, password))
    choose_folder()
