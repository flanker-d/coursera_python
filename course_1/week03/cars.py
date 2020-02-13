import csv
import os

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        root_ext = os.path.splitext(self.photo_file_name)
        return root_ext[1]

    @staticmethod
    def get_photo_file_ext_static(photo_file_name):
        root_ext = os.path.splitext(photo_file_name)
        return root_ext[1]

class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super(Car, self).__init__(brand, photo_file_name, carrying)
        self.car_type = "car"
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super(Truck, self).__init__(brand, photo_file_name, carrying)
        self.car_type = "truck"
        l, w, h = self._parse_whl(body_whl)
        self.body_width = float(w)
        self.body_height = float(h)
        self.body_length = float(l)

    def _parse_whl(self, body_whl):
        whl = body_whl.split('x')
        if len(whl) != 3:
            return (float(0), float(0), float(0))
        try:
            l = float(whl[0])
            w = float(whl[1])
            h = float(whl[2])
        except:
            return (float(0), float(0), float(0))
        return (l, w, h)

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super(SpecMachine, self).__init__(brand, photo_file_name, carrying)
        self.car_type = "spec_machine"
        self.extra = str(extra)

def _parse_car(row):
    car = {}
    car["car_type"] = row[0]
    car["brand"] = row[1]
    car["passenger_seats_count"] = row[2]
    car["photo_file_name"] = row[3]
    car["body_whl"] = row[4]
    car["carrying"] = row[5]
    car["extra"] = row[6]
    return car

def get_car_list(csv_filename):
    car_list = []
    try:
        with open(csv_filename) as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                try:
                    car = _parse_car(row)
                    type = str(car["car_type"])

                    if type in ["car", "truck", "spec_machine"]:
                        brand = str(car["brand"])
                        if len(brand) == 0:
                            continue
                        photo_file_name = str(car["photo_file_name"])
                        if len(photo_file_name) == 0:
                            continue
                        carrying = float(car["carrying"])
                        if carrying <= 0.0:
                            continue

                        file_ext = CarBase.get_photo_file_ext_static(photo_file_name)
                        if file_ext not in [".jpg", ".jpeg", ".png", ".gif"]:
                            continue

                        if type == "car":
                            passenger_seats_count = int(car["passenger_seats_count"])
                            if passenger_seats_count <= 0:
                                continue
                            car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))
                        elif type == "truck":
                            body_whl = str(car["body_whl"])
                            car_list.append(Truck(brand, photo_file_name, carrying, body_whl))
                        elif type == "spec_machine":
                            extra = str(car["extra"])
                            if len(extra) != 0:
                                car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))
                        else:
                            continue
                except:
                    continue
    except:
        pass

    return car_list

def _main():
    cars = get_car_list('cars.csv')
    print(cars)
    print(len(cars))

    for car in cars:
        print(type(car))
        print(isinstance(car.carrying, float))
        print(isinstance(car.carrying, float))

    print(cars[0].passenger_seats_count)

    print(cars[1].get_body_volume())

    cars = get_car_list('no_valid_cars.csv')
    print(cars)
    print(len(cars))

if __name__ == "__main__":
    _main()