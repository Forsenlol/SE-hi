import os
import re
import face_recognition as FC
from PIL import Image
import cv2
from glob import glob

def face_rec(paths = ['au_photos', 'csc_photos', 'itmo_photos'],
            user_photo_path = "/home/robez/Desktop/me.jpg"):

    img_lst = []

    for path in paths:
        img_lst.extend(glob(os.path.join(path, "*")))

    class CompareImage(object):

        def __init__(self, image_1_path, image_2_path):
            self.minimum_commutative_image_diff = 1
            self.image_1_path = image_1_path
            self.image_2_path = image_2_path

        def compare_image(self):
            image_1 = cv2.imread(self.image_1_path, 0)
            image_2 = cv2.imread(self.image_2_path, 0)
            commutative_image_diff = self.get_image_difference(image_1, image_2)

            if commutative_image_diff < self.minimum_commutative_image_diff:
                #print ("Matched")
                return commutative_image_diff
            return False #random failure value

        @staticmethod
        def get_image_difference(image_1, image_2):
            first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
            second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

            #метод гистограмм
            img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
            #метод сопоставления с образцом
            img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
            img_template_diff = 1 - img_template_probability_match

            # в общей разнице между картинками 10% учитывается методом гистограмм,
            # а 90% - метод сопоставления с образцом
            commutative_image_diff = (img_hist_diff / 10) + img_template_diff
            return commutative_image_diff


    user_face_match = {}

    user_name = "user"

    for i in img_lst:

        # unk_person_name = re.search('(?<=[\/]).*(?=[\.]png)',i).group()
        # если фотки в формате png
        temp = os.path.basename(i)
        if temp.endswith(".png"):
            unk_person_name = os.path.basename(i)[:-4]
        # если в .jpeg
        else:
            unk_person_name = os.path.basename(i)[:-5]


        compare_image = CompareImage(user_photo_path, i)
        img_diff = compare_image.compare_image()

        if img_diff == False:
            continue
        else:
            img_sim = abs(1 - img_diff)
            if img_diff < 0.8:

                new_value = [unk_person_name, img_sim]
                if user_face_match.get(user_name):
                    user_face_match[user_name].append(new_value)
                else:
                    user_face_match[user_name] = [new_value]

    # сортировка по матчингу от 0 до 1
    for k, v in user_face_match.items():
        v.sort(key=lambda x: x[1], reverse=True)
        v = v[0]

    user_match = v[0]
    return user_match
    # и найти соответсвующую картинку и показать
    # откроется только 1 картинка фиксированно
    # for path in paths:
    #     try:
    #         x = Image.open(os.path.join(path, user_match + ".png"))
    #         return user_match, x.show()
    #     except:
    #         continue