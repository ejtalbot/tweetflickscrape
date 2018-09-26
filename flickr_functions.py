import requests
from datetime import datetime, timedelta

#Flickr API Info
flickrKey= "9d0358bdb316fb63337122f6d5f8a8a5"
flickrSecret= "6b33cdb8f950b78a"

#gets the current date
current_datetime = datetime.now()
minimumSearchDate = current_datetime.date() - timedelta(30)

#returns a dictionary of the  of the photo ids
def flickr_photo_ids():
    baseUrl = "https://api.flickr.com/services/rest/"
    params = {
        "method": "flickr.photos.search",
        "api_key": flickrKey,
        "min_upload_date": minimumSearchDate,
        "media": "photos",
        "format": "json",
        "nojsoncallback": "1",
        "tags": "#dctech",
        "page": 1,
        "extras" : "count_comments"
    }
    #get a list of the photos that match the query defined in the parameters
    photoLibrary = requests.get(baseUrl, params=params).json()['photos']
    listOfPhotos = photoLibrary['photo']
    #add the results to a dictionary where the keys are the count of comments and values are the urls
    dictOfPhotos = {}
    flickr_photo_comment_dict(listOfPhotos, dictOfPhotos)
    totalPages = photoLibrary['pages']
    currentPage = int(photoLibrary['page'])
    #iterate through all pages of results and add to the dictionary of photos
    while(currentPage<totalPages):
        currentPage = currentPage + 1
        params['page'] = currentPage
        photoLibrary = requests.get(baseUrl, params=params).json()['photos']
        listOfPhotos = photoLibrary['photo']
        flickr_photo_comment_dict(listOfPhotos, dictOfPhotos)
    return dictOfPhotos

#modifies the dictionary to add new values (and keys where applicable)
def flickr_photo_comment_dict(photoList, photoDict):
    for photo in photoList:
        #get the parameters to construct the source url
        farm = photo['farm']
        serverId = photo['server']
        photoId = photo['id']
        secret = photo['secret']
        #construct the source url with the below function
        sourceUrl = create_source_url(farm, serverId, photoId, secret)
        #add the value to the dictionary, inserting a new key if necessary, otherwise appending to list with existing key
        if int(photo['count_comments']) not in photoDict:
            photoDict[int(photo['count_comments'])] = [sourceUrl]
        else:
            photoDict[int(photo['count_comments'])].append(sourceUrl)

#create the source url for the photo
def create_source_url(farm, serverId, photoId, secret):
    return "https://farm" + str(farm) + ".staticflickr.com/" + str(serverId) + "/" + str(photoId) + "_" + str(secret) + ".jpg"
