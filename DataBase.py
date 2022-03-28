"""
experiment:
    self.id = id
    self.type = n0
    self.meta = {metadata}
    self.children = [descendência]

element:
    self.id = id
    self.type = nx
    self.meta = {metadata}
    self.family = {ascendência1 : descendência1
                   ascendência2 : descendência2}

datum:
    self.id = ascendência
    self.type = d
    self.meta = {metadata}
    self.data = data

structure = ['n1', 'n2', n3', ...]

index = [

        n0 : {n0.id : n0}

        n1 : {n1_1.id : n1_1,
              n1_2.id : n1_2,
              n1_3.id : n1_3, ...}

        n2 : {n2_1.id : n2_1,
              n2_2.id : n2_2,
              n2_3.id : n2_3, ...}

        n3 : {n3_1.id : n3_1,
              n3_2.id : n3_2,
              n3_3.id : n3_3, ...}

        ...

        d : {d1.id : d1.data,
             d2.id : d2.data,
             d3.id : d3.data, ...}

        ]
"""
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import datetime
import itertools
import pickle
import fuckit
import h5py
import time
import glob
import csv
import sys


class experiment:
    """."""
    index = []
    structure = []

    def __init__(self, id, type_names, *children, **meta):
        """
        Initiates the basis for data uploading.
        :param id: Experiment name
        :param type_names: structure list = ['n1', 'n2', n3', ...]
        :param children: (optional) [n1_1, n1_2, n1_3, ...]
        :param meta: (optional) label1 = 'value', label2 = 'value, ...
        """
        self.structure.append('Experiment')
        for type in type_names:
            self.structure.append(type)
        self.structure.append('data')

        for _ in range(len(type_names) + 2):
            self.index.append({})

        self.index = self.index
        self.structure = self.structure

        self.id = id
        self.type = 0
        self.index[0][id] = self

        self.children = []
        if children != ():
            self.add_branch(*children)

        self.meta = {}
        if meta != {}:
            self.add_meta(**meta)

    def add_meta(self, **meta):
        """
        Adds metadata to given element.
        :param meta: label1 = 'value', label2 = 'value, ...
        """
        for key, values in meta.items():
            self.meta[key] = values

    def del_meta(self, *keys):
        """
        Deletes metadata from given element with certain label.
        :param keys:  [label1, label2, ...]
        """
        [self.meta.pop(key) for key in keys]

    def add_branch(self, family):
        """
        Adds branch to given element (nx).
        nx must be omitted from family values
        :param family: [n0, n1_a, ... , n(x-1)_b, n(x+1)_c], [n0, n1_d, ... , n(x-1)_e, n(x+1)_f], ...
        """
        [self.children.append(child) for child in family if child not in self.children]

    def del_branch(self, *children):
        """
        Deletes branch from given element (nx). \n
        If given children, said children are deleted from experiment \n
        If given nothing, all family is cleared from experiment \n
        A child value be of type n(x+1)
        :param children: (optional) [ch1, ch2, ...]
        """
        if children is None:
            self.children = []
        else:
            [self.children.pop(self.children.index(child)) for child in children]

    def del_node(self):
        """
        Deletes given element (nx) from experiment.
        To be done
        """
        pass

    def get_id(self):
        """
        Used to retrieve a element's given name (id).
        :return: element id
        """
        return self.id

    @staticmethod
    def show_index():
        """
        Gives overview of the experiment, showing every instance of every structure type.
        """
        print('\\-/*\\-/*\\-/ INDEX \\-/*\\-/*\\-/')
        for n, type in enumerate(experiment.index):
            print(experiment.structure[n])
            for key, value in type.items():
                empty = ''
                (print(f'\t{list(parent.get_id() for parent in key if parent is not empty)[1:]}') if n == len(
                    experiment.index) - 1 else print(f'\t{key}'))

    @staticmethod
    def get_node(id, type):
        """
        Used to retrieve a element from its name and type.
        :param id: element's given name (id)
        :param type: element's type in number
        :return: element
        """
        return experiment.index[type][id]

    @staticmethod
    def exists(id, type):
        try:
            element.get_node(id, type)
            return True
        except KeyError:
            return

    def show(self, *depth):
        """
        Shows metadata and family from given element.
        :param depth: indentation value
        """
        print(f'--- {self.structure[self.type]} ---')
        find, tind, ntind = '', '', ''
        for _ in depth:
            find = depth[0] * '\t'

        tind = find + f'|-{self.type}-| '
        ntind = find + '\t  '
        print(f'{tind}ID: {self.id}')
        for key, value in self.meta.items():
            print(f'{ntind}{key} {value}')
        x = [child.get_id() for child in self.children]
        print(f'{ntind} | {x}')
        print(f'{ntind}  -------')

    def show_type(self, *type_list):
        """
        Shows metadata and family from given element's type.
        """
        if type_list == ():
            [element.show() for element in self.index[self.type].values()]
        else:
            for type in type_list:
                [element.show() for element in self.index[type].values()]

    def checks_meta(self, key, value):
        """
        Checks if a single key:value pair applies to element's metadata or id
        :param key, value: given in checks()
        :return: True if applies, False otherwise
        """
        if self.id == value:
            return True
        if key not in self.meta:
            return value == '-'
        if not isinstance(value, tuple) and not isinstance(value, list):
            if ':' not in value:
                return value == '+' or self.meta[key] == value
            subvalue = value.split(':')
            print(subvalue)
        if value[0] == '':
            return self.meta[key] < value[1]
        if value[1] == '':
            return self.meta[key] > value[0]
        return value[0] < self.meta[key] < value[1]

    def checks(self, conditions):
        """
        Evaluates if all conditions apply to a certain element's and parents' metadata \n
        :param conditions: given in filtering()
        :return: True if all applies, False otherwise
        """
        for label, value in conditions.items():
            if '_' in label and label[-2] == '_':
                n = self.id[int(label[-1])]
                if n == '':
                    return
                if not n.checks_meta(label[:-2], value):
                    return
            else:
                if not self.checks_meta(label, value):
                    return
        return True

    def filtering(self, **conditions):
        """
        Filters through all datum's parents
        labels should contain a '_n' in the end with n being the type of data to apply certain condition to
        label = value verifies if label exists with certain value \n
        label = '+' verifies if label exists \n
        label = '-' verifies if label does not exist \n
        label = (value1,value2) verifies if label's value is between given v1 and v2 (inclusive) \n
        value1 = ' ' if lower or value2 = ' ' if upper bound does not matter \n
        :param conditions: Conditions to be evaluated
        :return: list of filtered data
        """
        return [element for element in self.index[-1].values() if element.checks(conditions)]

    def save(self, filename):
        with open(f'{filename}.dtf', 'wb') as out:
            pickle.dump(self.index, out, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename):
        with open(f'{filename}.dtf', 'rb') as input:
            return list(pickle.load(input)[0].values())[0]


class element(experiment):
    """."""

    def __init__(self, id, type, *family, **meta):
        """
        Initiates a element. \n
        If adding a branch, nx must be omitted from family values \n
        :param id: Node's name
        :param type: Node's type in number (x)
        :param family: (optional) [n0, n1_a, ... , n(x-1)_b, n(x+1)_c], [n0, n1_d, ... , n(x-1)_e, n(x+1)_f], ...
        :param meta: (optional) label1 = 'value', label2 = 'value, ...
        """

        self.id = id
        self.type = type

        if id not in self.index[type]:
            self.index[type][id] = self
            self.family = {}
            self.meta = {}

        self.family = self.index[type][id].family
        self.meta = self.index[type][id].meta

        self.index = self.index
        self.structure = self.structure

        if family != ():
            self.add_branch(*family)

        if meta != {}:
            self.add_meta(**meta)

    def add_branch(self, family):
        """
        Adds branch to given element (nx).
        nx must be omitted from family values
        :param family: [n0, n1_a, ... , n(x-1)_b, n(x+1)_c], [n0, n1_d, ... , n(x-1)_e, n(x+1)_f], ...
        """
        child = family[-1]
        parents = family[:-1]
        if parents not in self.family:
            self.family[parents] = [child]
        else:
            if child not in self.family[parents]:
                self.family[parents].append(child)

        family[-2].add_branch(family[:-2] + (self,))

    def del_branch(self, *, parent=None, children=None):
        """
        Deletes branch from given element (nx). \n
        If given parent and children, those specific combos are deleted \n
        If given only parent, all children from said parent are also deleted \n
        If given only children, said children are deleted from every parent \n
        If given nothing, all family is cleared from element \n
        A parent value must carry all ancestry: (n0, n1_a, ... , n(x-1)_b) \n
        A child value be of type n(x+1)
        :param parent: (optional) [(p1), (p2), ...]
        :param children: (optional) [ch1, ch2, ...]
        """
        if parent is None:
            if children is None:
                self.family = {}
            else:
                for child in children:
                    [self.family[parent].remove(child) for parent in self.family if child in self.family[parent]]
        else:
            if children is None:
                self.family.pop(parent, None)
            else:
                [self.family[parent].remove(child) for child in children if child in self.family[parent]]

    def show(self, *depth):
        """
        Shows metadata and family from given element.
        :param depth: indentation value
        """
        print(f'--- {self.structure[self.type]} ---')
        find, tind, ntind = '', '', ''
        for _ in depth:
            find = depth[0] * '\t'

        tind = find + f'|-{self.type}-| '
        ntind = find + '\t  '
        print(f'{tind}ID: {self.id}')
        for key, value in self.meta.items():
            print(f'{ntind}{key} {value}')
        if self.type == len(self.structure) - 2:
            for parents in self.family:
                print(f'{ntind} | {list(map(element.get_id, parents))} - Data')
        else:
            for parents in self.family:
                printparents = parents[1:] if len(parents) > 1 else parents
                print(
                    f'{ntind} | {list(map(element.get_id, printparents))} - {list(map(element.get_id, self.family[parents]))}')
        print(f'{ntind}  -------')


class datum(element):
    """."""

    def __init__(self, *family, **meta):
        """
        Initiates a datum.
        :param parents: Data's ancestry (n0, n1_a, ... , n(x-1)_b)
        :param dt: data array
        :param meta: (optional) label1 = 'value', label2 = 'value, ...
        """
        self.id = family[:-1]
        self.family = {}
        self.type = len(self.structure) - 1
        self.data = list(itertools.chain(*family[-1]))
        self.index[self.type][family[:-1]] = self

        self.index = self.index
        self.structure = self.structure

        self.meta = {}
        if meta != {}:
            self.add_meta(**meta)

        family[-2].add_branch(family[:-2] + (self,))

    def plot(self):
        """
        Plots data
        """
        plt.plot(self.data)
        plt.show()

    def show(self, *depth):
        """
        Shows metadata and family from given element.
        :param depth: indentation value
        """
        print(f'--- {self.structure[self.type]} ---')
        find, tind, ntind = '', '', ''
        for _ in depth:
            find = depth[0] * '\t'

        tind = find + f'|-{self.type}-| '
        ntind = find + '\t  '
        parents = [element.get_id() for element in self.id]
        print(f'{tind}ID: {parents[1:]}')
        for key, value in self.meta.items():
            print(f'{ntind}{key} {value}')


# noinspection PyUnreachableCode
@fuckit
def convert(n):
    return int(n)
    return float(n)
    t = time.strptime(n, '%dd%Hh%Mm%Ss')
    return timedelta(days=t.tm_mday,
                     hours=t.tm_hour,
                     minutes=t.tm_min,
                     seconds=t.tm_sec)
    t = time.strptime(n, '%Hh%Mm%Ss')
    return timedelta(hours=t.tm_hour,
                     minutes=t.tm_min,
                     seconds=t.tm_sec)
    t = time.strptime(n, '%Mm%Ss')
    return timedelta(minutes=t.tm_min,
                     seconds=t.tm_sec)
    t = time.strptime(n, '%Ss')
    return timedelta(seconds=t.tm_sec)
    return n


# Example
# structure = ['E', 'S', 'P', 'D', 'C']
#
# e = experiment('e1', structure)
# s1 = element('S1', 1, datetime=datetime(2021, 2, 4), teste=1)
# s2 = element('S2', 1, datetime=datetime(2021, 11, 5, 11, 46), teste=0)
# p1 = element('P1', 2, name='Ze', age=32)
# p2 = element('P2', 2, name='Didi', age=22)
# p3 = element('P3', 2, name='To', age=44)
# d1 = element('D1', 3, s_rate=60)
# d2 = element('D2', 3, s_rate=1000)
# d3 = element('D3', 3, s_rate=240, teste=735)
# c1_1 = element('D1Ch1', 4, resolution=0.01, unit='V')
# c1_2 = element('D1Ch2', 4, resolution=0.001, unit='V')
# c2_1 = element('D2Ch1', 4, resolution=0.01, unit='A')
# c2_2 = element('D2Ch2', 4, resolution=0.1, unit='mA')
# c3_1 = element('D3Ch1', 4, resolution=0.01, unit='V')
# c4_1 = element('Ch4', 4, resolution=1, unit='mV')
# data1 = datum(e, s2, p1, d1, c1_1, [0, 1, 2, 3, 4], name='dt2', n=4)
# data2 = datum(e, s1, p2, d2, c1_2, [2, 8, 5, 3, 6], na_me='dt1', n=4)
# data3 = datum(e, s1, p2, d2, c2_1, [4, 7, 2, 7, 2])
# data4 = datum(e, s1, p2, d3, c1_2, [4, 7, 3, 2, 2])
# data5 = datum(e, s2, p3, d3, c3_1, [3, 6, 8, 2, 1])
# data6 = datum(e, s2, p2, d2, c4_1, [4, 7, 2, 7, 2], name='dt3')
# data7 = datum(e, s2, p2, d2, c2_2, [4, 7, 3, 2, 2])
# data8 = datum(e, s2, p1, d3, c3_1, [3, 6, 8, 2, 1])


# PATRICIA
# structure = ['Film', 'Person', 'Device', 'Channel']
#
# e = experiment('Patricia\'s films', structure,
#                Description='A person\'s EDA and PPG values are measured while watching a film',
#                Goal='Testing the database\'s structure')
#
# for film_id in ['f1', 'f2', 'f3']:
#
#     film = element(f'{film_id}', 1)
#
#     files = glob.glob(f'data/{film_id}/*.hdf5')
#     for person_id in files:
#         person = element(person_id[:-5].split('\\')[1], 2)
#
#         file = h5py.File(person_id, 'r')
#         for device_id in [device for device in list(file.keys()) if device not in ('LOGs', 'Flags')]:
#             device = element(f'{device_id}', 3)
#
#             channels = file[device_id]['EDA'].shape[1]
#             for channel_id in range(channels):
#                 channel = element(f'{device_id}_{channel_id}', 4)
#                 d = [file[device_id]['EDA'][:, channel_id]]
#
#                 # datum(e, film, person, device, channel, d)
#
# for meta_file in glob.glob(f'metadata/*.csv'):
#     type = int(meta_file.split('\\')[1][0])
#     with open(meta_file, 'r', encoding='utf-8-sig') as file:
#         file = csv.reader(file)
#         header = next(file)
#         while True:
#             try:
#                 data = [convert(value) for value in next(file)]
#             except StopIteration:
#                 break
#             id = str(data[0])
#             if element.exists(id, type):
#                 metadata = {key: value for key, value in zip(header[1:], data[1:])}
#                 element.get_node(id, type).add_meta(**metadata)
#
# e.save('dataless_teste')

e = experiment.load('teste')
#
for data in e.filtering(Device_3='R-IoT',
                        id_4='10_5'):
    data.plot()
