import requests
import json
import pygame
from PIL import Image
from random import randrange
GLOBAL_TILE_SIZE = 512


class SearchArt:

    def getImageList(self):
        rk_api_token = 'aTcoXoCh'
        rk_url_postfix = '&q='

        format_json = 'json'
        rk_type_paint = 'painting'
        rk_type_material = 'canvas'
        rk_url_call_end = '\''
        rk_api_url_base_prefix = 'https://www.rijksmuseum.nl/api/en/collection?key=' + rk_api_token
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(rk_api_token)}

        query_params = {"q": self.search_value, "format": format_json, "object_type": rk_type_paint,
                       "material": rk_type_material}

        response = requests.request("GET", rk_api_url_base_prefix, headers=headers, params=query_params)
        if response.status_code == 200:
            print('success')
            print(response.text)

            json_obj = json.loads(response.content.decode('utf-8'))
            print(json_obj['artObjects'])
            art_list = json_obj['artObjects']

            if len(art_list) > 0:
                art_index = randrange(len(art_list))
            print(art_index)
            return art_list[art_index]
        else:
            print('error ' + response.status_code)

    def __init__(self, mood_str):
        self.currentState = None
        self.search_value = mood_str

class GetArtTiles:
    print('get the one')

    def __init__(self, art_dict):
        self.currentState = None
        self.art_dict = art_dict

    def getArtImage(self):
        rk_api_token = 'aTcoXoCh'
        rk_url_postfix = '&q='
        # get random of list
        # String prefix = "https://www.rijksmuseum.nl/api/en/collection/"+params[0].get_object_number()+"/tiles?format=json&key=";
        format_json = 'json'
        object_number = self.art_dict.get("objectNumber","")
        rk_type_paint = 'painting'
        rk_type_material = 'canvas'
        rk_url_call_end = '\''
        rk_api_url_base_prefix = 'https://www.rijksmuseum.nl/api/en/collection/'+object_number+'/tiles'+'?key=' + rk_api_token
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(rk_api_token)}

        query_params = { "format": format_json }

        response = requests.request("GET", rk_api_url_base_prefix, headers=headers, params=query_params)
        if response.status_code == 200:
            print('success')
            print(response.text)
            json_obj = json.loads(response.content.decode('utf-8'))
            print(json_obj)
            return (json_obj)
        else:
            print ('error '+response.status_code + ' '+response.text)



class GetArtImage:

    def __init__(self, art_obj,width,height):
        self.currentState = None
        self.art_obj = art_obj
        self.width = width
        self.height = height

    # TODO add assert for error here
    def searchForLevel(self, image_levels):
        for l in image_levels:
            if l['name'] == 'z3':
                return l
        return image_levels[0]

    def getBitmapFromTiles(self):

        # choose the level by name z0 is the largest resolution z6 is the lowest resolution
        #   look for z3 or z4
        image_levels = self.art_obj['levels']
        art_level = self.searchForLevel(image_levels)
        final_image = Image.new('RGB', (art_level['width'], art_level['height']))
        for i in art_level['tiles']:
            tmp_image = Image.open(requests.get(i['url'], stream=True).raw)
            tmp_x = i['x'] * GLOBAL_TILE_SIZE
            tmp_y = i['y'] * GLOBAL_TILE_SIZE
            print('image w h')
            print(final_image.width)
            print(final_image.height)
            final_image.paste(tmp_image,(tmp_x,tmp_y))

        grid_image = final_image.resize((int(self.width), int(self.height)),Image.LANCZOS)
        mode = grid_image.mode
        size = grid_image.size
        data = grid_image.tobytes()

        py_image = pygame.image.fromstring(data, size, mode)
        return py_image, grid_image

    # cut the image to tiles and return them as two dimentianal array
    # im_crop = im.crop((100, 75, 300, 150))
    # calculate # tiles : regular and level specific
    # calculate per col and per line

    def getImageTiles(self):
        w, h = 8, 5;
        matrix = [[0 for x in range(w)] for y in range(h)]
        return matrix