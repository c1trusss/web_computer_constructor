from flask_restful import reqparse, abort, Resource
from flask import jsonify

from data import db_session
from data.components import *

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('brand', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)


def abort_if_component_not_found(component):
    if component not in ('cpu', 'memory', 'disk', 'gpu', 'motherboard', 'core', 'power', 'cpu_coolers'):
        abort(404, message="Component not found")


class ComponentResource(Resource):

    def get(self, component_class, component_id):
        abort_if_component_not_found(component_class)
        session = db_session.create_session()
        component = session.query(component_class).get(component_id)
        return jsonify(
            {component_class: component.to_dict(only=('title', 'cost'))}
        )


class ComponentListResource(Resource):

    def get(self, component_class):

        abort_if_component_not_found(component_class)

        component = None
        match component_class:
            case 'cpu':
                component = CPU
            case 'gpu':
                component = GPU
            case 'core':
                component = Core
            case 'power':
                component = Power
            case 'disk':
                component = Disk
            case 'cpu_coolers':
                component = CPUCoolers
            case 'motherboard':
                component = Motherboard
            case 'ram':
                component = RAM

        session = db_session.create_session()
        components = session.query(component).all()
        return jsonify(
            {
                component_class: [item.to_dict(only=('id', 'title', 'cost')) for item in components]
            }
        )

    def post(self, component_class):

        abort_if_component_not_found(component_class)

        args = parser.parse_args()
        session = db_session.create_session()

        component = None
        match component_class:
            case 'cpu':
                component = CPU()
                component.title = args['title']
                component.brand = args['brand']
                component.socket = args['socket']
                component.cpu_group = args['cpu_group']
                component.delivery_type = args['delivery_type']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']
            case 'gpu':
                component = GPU()
                component.title = args['title']
                component.brand = args['brand']
                component.memory = args['memory']
                component.developer = args['developer']
                component.memory_type = args['memory_type']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']
            case 'core':
                component = Core()
                component.title = args['title']
                component.brand = args['brand']
                component.core_type = args['core_type']
                component.form_factor = args['form_factor']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']
            case 'cpu_coolers':
                component = CPUCoolers()
                component.title = args['title']
                component.brand = args['brand']
                component.tdp = args['tdp']
                component.socket = args['socket']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']
            case 'disk':
                component = Disk()
                component.title = args['title']
                component.brand = args['brand']
                component.capacity = args['capacity']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']
            case 'motherboard':
                component = Motherboard()
                component.title = args['title']
                component.brand = args['brand']
                component.socket = args['socket']
                component.chipset = args['chipset']
                component.form_factor = args['form_factor']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']
            case 'power':
                component = Power()
                component.title = args['title']
                component.brand = args['brand']
                component.power = args['power']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']
            case 'memory':
                component = RAM()
                component.title = args['title']
                component.brand = args['brand']
                component.memory = args['memory']
                component.memory_type = args['memory_type']
                component.freq = args['freq']
                component.cost = args['cost']
                component.link = args['link']
                component.image = args['image']

        session.add(component)
        session.commit()
        return jsonify({'id': component.id})
