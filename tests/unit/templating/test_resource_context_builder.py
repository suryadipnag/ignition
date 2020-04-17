import unittest
from ignition.templating.resource_context_builder import ResourceContextBuilder
from ignition.utils.propvaluemap import PropValueMap

class TestResourceContextBuilder(unittest.TestCase):

    def __example_values(self):
        system_properties = {
            'sysA': 'A',
            'sysB': 'B'
        }
        properties = {
            'propA': 'A Prop'
        }
        deployment_location = {
            'name': 'Test',
            'type': 'Kubernetes',
            'properties': {
                'dlPropA': 'A DL Prop'
            }
        }
        return system_properties, properties, deployment_location

    def test_init(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    def test_init_with_prop_value_maps(self):
        system_properties, properties, deployment_location = self.__example_values()
        system_properties = PropValueMap(system_properties)
        properties = PropValueMap(properties)
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    def test_add_properties(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        builder.add_properties({'propB': 'B Prop', 'propC': 'C Prop'})
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'propB': 'B Prop',
            'propC': 'C Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    def test_add_properties_from_prop_value_map(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        builder.add_properties(PropValueMap({'propB': 'B Prop', 'propC': 'C Prop'}))
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'propB': 'B Prop',
            'propC': 'C Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    
    def test_add_property(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        builder.add_property('propB', 'B Prop')
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'propB': 'B Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    def test_add_system_properties(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        builder.add_system_properties({'sysC': 'C', 'sysD': 'D'})
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B',
                'sysC': 'C',
                'sysD': 'D'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    def test_add_system_properties_from_prop_value_map(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        builder.add_system_properties(PropValueMap({'sysC': 'C', 'sysD': 'D'}))
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B',
                'sysC': 'C',
                'sysD': 'D'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    def test_add_system_property(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        builder.add_system_property('sysC', 'C')
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B',
                'sysC': 'C'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })

    def test_add_properties_with_reserved_system_property_keyword(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        with self.assertRaises(ValueError) as context:
            builder.add_properties({'systemProperties': 'ThisPropertyIsNotAllowed'})
        self.assertEqual(str(context.exception), 'property with name \'systemProperties\' cannot be used as this is a reserved word')

    def test_add_properties_with_reserved_deployment_location_inst_keyword(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        with self.assertRaises(ValueError) as context:
            builder.add_properties({'deploymentLocationInst': 'ThisPropertyIsNotAllowed'})
        self.assertEqual(str(context.exception), 'property with name \'deploymentLocationInst\' cannot be used as this is a reserved word')

    def test_add_property_with_reserved_system_property_keyword(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        with self.assertRaises(ValueError) as context:
            builder.add_property('systemProperties', 'ThisPropertyIsNotAllowed')
        self.assertEqual(str(context.exception), 'property with name \'systemProperties\' cannot be used as this is a reserved word')

    def test_add_property_with_reserved_deployment_location_inst_keyword(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        with self.assertRaises(ValueError) as context:
            builder.add_property('deploymentLocationInst', 'ThisPropertyIsNotAllowed')
        self.assertEqual(str(context.exception), 'property with name \'deploymentLocationInst\' cannot be used as this is a reserved word')

    def test_set_deployment_location(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        new_deployment_location = {
            'name': 'Alternative',
            'type': 'Docker',
            'properties': {
                'dlPropA': 'Alternative DL Prop'
            }
        }
        builder.set_deployment_location(new_deployment_location)
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Alternative',
                'type': 'Docker',
                'properties': {
                    'dlPropA': 'Alternative DL Prop'
                }
            }
        })

    def test_add_deployment_location_property(self):
        system_properties, properties, deployment_location = self.__example_values()
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        builder.add_deployment_location_property('dlPropB', 'B DL Prop')
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop',
                    'dlPropB': 'B DL Prop'
                }
            }
        })

    def test_deployment_location_property_not_hidden(self):
        system_properties, properties, deployment_location = self.__example_values()
        properties['deploymentLocation'] = 'Test'
        builder = ResourceContextBuilder(system_properties, properties, deployment_location)
        self.assertEqual(builder.result, {
            'propA': 'A Prop',
            'deploymentLocation': 'Test',
            'systemProperties': {
                'sysA': 'A',
                'sysB': 'B'
            }, 
            'deploymentLocationInst': {
                'name': 'Test',
                'type': 'Kubernetes',
                'properties': {
                    'dlPropA': 'A DL Prop'
                }
            }
        })