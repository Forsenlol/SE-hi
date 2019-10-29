import os
import cv2
from glob import glob
from config import PHOTO_PATH


def face_rec(user_photo_path):
    img_lst = []

    for path in PHOTO_PATH:
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
                # print ("Matched")
                return commutative_image_diff
            return False  # random failure value

        @staticmethod
        def get_image_difference(image_1, image_2):
            first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
            second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

            # метод гистограмм
            img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
            # метод сопоставления с образцом
            img_template_probability_match = \
            cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
            img_template_diff = 1 - img_template_probability_match

            # в общей разнице между картинками 10% учитывается методом гистограмм,
            # а 90% - метод сопоставления с образцом
            commutative_image_diff = (img_hist_diff / 10) + img_template_diff
            return commutative_image_diff

    user_face_match = []

    for i in img_lst:

        # если фотки в формате png / jpg
        temp = os.path.basename(i)
        if temp.endswith(".png") or temp.endswith(".jpg"):
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

            if img_sim > 0.2:
                new_value = (unk_person_name, img_sim)
                user_face_match.append(new_value)

    # сортировка по матчингу от 0 до 1
    # print(user_face_match)
    # print(user_face_match.sort(key=lambda x: x[1], reverse=True))

    user_match = user_face_match[0][0]
    return user_match + '.png', int(user_match[:user_match.index('_')])