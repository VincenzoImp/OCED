from typing_extensions import override
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from copy import deepcopy
import json


class __Qualifier:
    '''
    Class to handle qualifiers

    Attributes
    ----------
    qualifier_name : str
        Qualifier name
    qualifier_type : str
        Qualifier type
    
    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, qualifier_name, qualifier_type):
        '''
        Initialize __Qualifier object

        Parameters
        ----------
        qualifier_name : str
            Qualifier name
        qualifier_type : str
            Qualifier type
        
        Returns
        -------
        None

        Raises
        ------
        None
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # initialize
        self.__qualifier_name = qualifier_name
        self.__qualifier_type = qualifier_type

    @property
    def qualifier_name(self):
        '''
        Get qualifier name

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Qualifier name
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__qualifier_name

    @property
    def qualifier_type(self):
        '''
        Get qualifier type

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Qualifier type
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__qualifier_type

    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        # to be implemented in child classes
        pass

    def __update_tables(self, OCED_model, qualifier_index):
        # to be implemented in child classes
        pass

    def __log(self):
        # to be implemented in child classes
        pass


class create_object(__Qualifier):
    '''
    Class to handle create_object qualifiers
    
    Attributes
    ----------
    object_id : str
        Object id
    object_type : str
        Object type
    
    Methods
    -------
    None
    
    Notes
    -----
    None
    
    Examples
    --------
    None
    '''

    def __init__(self, object_id, object_type):
        '''
        Initialize create_object qualifier

        Parameters
        ----------
        object_id : str
            Object id
        object_type : str
            Object type
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_id is not a string
            - If object_type is not a string

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_id
        if not isinstance(object_id, str):
            raise TypeError('object_id must be a string')
        # check object_type
        if not isinstance(object_type, str):
            raise TypeError('object_type must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'CREATE')
        self.__object_id = object_id
        self.__object_type = object_type

    @property
    def object_id(self):
        '''
        Get object id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object id

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        return self.__object_id
    
    @property
    def object_type(self):
        '''
        Get object type

        Parameters
        ----------
        None

        Returns
        -------
        str
            Object type
        
        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        return self.__object_type
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object id already exists before execute create_object qualifier

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check if object_id can be created
        if self.__object_id in current_state['object']:
            raise ValueError(f'{self.__object_id} must not be an existing object id before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object'][self.__object_id] = {
            'type': self.__object_type,
            'existency': True,
            'object_relation_ids': [],
            'object_attribute_value_ids': []
        }
        involved_ids['object'].add(self.__object_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index

        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object table of OCED model
        row = {
            'object_id': [self.__object_id], 
            'object_type': [self.__object_type], 
            'object_existency': [True]
        }
        OCED_model._OCED__object = pd.concat([OCED_model._OCED__object, pd.DataFrame(row)], ignore_index=True)
        # update object_type table of OCED model
        if self.__object_type not in OCED_model._OCED__object_type['object_type'].values:
            row = {
                'object_type': [self.__object_type]
            }
            OCED_model._OCED__object_type = pd.concat([OCED_model._OCED__object_type, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter], 
            'object_id': [self.__object_id], 
            'qualifier_type': [self.qualifier_type], 
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object = pd.concat([OCED_model._OCED__event_x_object, pd.DataFrame(row)], ignore_index=True)

    @override
    def __log(self):
        '''
        Get log create_object qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_id': self.__object_id,
                'object_type': self.__object_type
            }
        }


class create_object_relation(__Qualifier):
    '''
    Class to handle create_object_relation qualifiers
    
    Attributes
    ----------
    object_relation_id : str
        Object relation id
    from_object_id : str
        From object id
    to_object_id : str
        To object id
    object_relation_type : str
        Object relation type
    
    Methods
    -------
    None
    
    Notes
    -----
    None
    
    Examples
    --------
    None
    '''

    def __init__(self, object_relation_id, from_object_id, to_object_id, object_relation_type):
        '''
        Initialize create_object_relation qualifier

        Parameters
        ----------
        object_relation_id : str
            Object relation id
        from_object_id : str
            From object id
        to_object_id : str
            To object id
        object_relation_type : str
            Object relation type
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_relation_id is not a string
            - If from_object_id is not a string
            - If to_object_id is not a string
            - If object_relation_type is not a string
        ValueError
            - If from_object_id is equal to to_object_id
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_relation_id
        if not isinstance(object_relation_id, str):
            raise TypeError('object_relation_id must be a string')
        # check from_object_id
        if not isinstance(from_object_id, str):
            raise TypeError('from_object_id must be a string')
        # check to_object_id
        if not isinstance(to_object_id, str):
            raise TypeError('to_object_id must be a string')
        # check object_relation_type
        if not isinstance(object_relation_type, str):
            raise TypeError('object_relation_type must be a string')
        # check if from_object_id and to_object_id are different
        if from_object_id == to_object_id:
            raise ValueError('from_object_id and to_object_id must be different')
        # initialize
        super().__init__(self.__class__.__name__, 'CREATE')
        self.__object_relation_id = object_relation_id
        self.__from_object_id = from_object_id
        self.__to_object_id = to_object_id
        self.__object_relation_type = object_relation_type

    @property
    def object_relation_id(self):
        '''
        Get object relation id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object relation id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_relation_id    
    
    @property
    def from_object_id(self):
        '''
        Get from object id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            From object id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__from_object_id
    
    @property
    def to_object_id(self):
        '''
        Get to object id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            To object id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__to_object_id
    
    @property
    def object_relation_type(self):
        '''
        Get object relation type

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Relation type
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_relation_type
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_relation_id already exists before execute create_object_relation qualifier
            - If to_object_id does not exist before execute create_object_relation qualifier
            - If from_object_id does not exist before execute create_object_relation qualifier
            
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_relation_id can be created
        if self.__object_relation_id in current_state['object_relation']:
            raise ValueError(f'{self.__object_relation_id} must not be an existing object_relation_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if self.__to_object_id not in current_state['object'] or current_state['object'][self.__to_object_id]['existency'] == False:
            raise ValueError(f'{self.__to_object_id} must be an existing to_object_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if self.__from_object_id not in current_state['object'] or current_state['object'][self.__from_object_id]['existency'] == False:
            raise ValueError(f'{self.__from_object_id} must be an existing from_object_id before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object_relation'][self.__object_relation_id] = {
            'type': self.__object_relation_type,
            'existency': True,
            'from_object_id': self.__from_object_id,
            'to_object_id': self.__to_object_id
        }
        current_state['object'][self.__from_object_id]['object_relation_ids'].append(self.__object_relation_id)
        current_state['object'][self.__to_object_id]['object_relation_ids'].append(self.__object_relation_id)
        involved_ids['object_relation'].add(self.__object_relation_id)
        
    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object_relation table of OCED model
        row = {
            'object_relation_id': [self.__object_relation_id], 
            'from_object_id': [self.__from_object_id], 
            'to_object_id': [self.__to_object_id], 
            'object_relation_type': [self.__object_relation_type], 
            'object_relation_existency': [True]
        }
        OCED_model._OCED__object_relation = pd.concat([OCED_model._OCED__object_relation, pd.DataFrame(row)], ignore_index=True)
        # update object_relation_type table of OCED model
        if self.__object_relation_type not in OCED_model._OCED__object_relation_type['object_relation_type'].values:
            row = {
                'object_relation_type': [self.__object_relation_type]
            }
            OCED_model._OCED__object_relation_type = pd.concat([OCED_model._OCED__object_relation_type, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object_relation table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter], 
            'object_relation_id': [self.__object_relation_id], 
            'qualifier_type': [self.qualifier_type], 
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_relation = pd.concat([OCED_model._OCED__event_x_object_relation, pd.DataFrame(row)], ignore_index=True)

    @override
    def __log(self):
        '''
        Get log create_object_relation qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_relation_id': self.__object_relation_id,
                'from_object_id': self.__from_object_id,
                'to_object_id': self.__to_object_id,
                'object_relation_type': self.__object_relation_type
            }
        }
    

class create_object_attribute_value(__Qualifier):
    '''
    Class to handle create_object_attribute_value qualifiers

    Attributes
    ----------
    object_attribute_value_id : str
        Object attribute value id
    object_id : str
        Object id
    object_attribute_name : str
        Object attribute name
    object_attribute_value : str
        Object attribute value

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_attribute_value_id, object_id, object_attribute_name, object_attribute_value):
        '''
        Initialize create_object_attribute_value qualifier

        Parameters
        ----------
        object_attribute_value_id : str
            Object attribute value id
        object_id : str
            Object id
        object_attribute_name : str
            Object attribute name
        object_attribute_value : str
            Object attribute value
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_attribute_value_id is not a string
            - If object_id is not a string
            - If object_attribute_name is not a string
            - If object_attribute_value is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_attribute_value_id
        if not isinstance(object_attribute_value_id, str):
            raise TypeError('object_attribute_value_id must be a string')
        # check object_id
        if not isinstance(object_id, str):
            raise TypeError('object_id must be a string')
        # check object_attribute_name
        if not isinstance(object_attribute_name, str):
            raise TypeError('object_attribute_name must be a string')
        # check object_attribute_value
        if not isinstance(object_attribute_value, str):
            raise TypeError('object_attribute_value must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'CREATE')
        self.__object_attribute_value_id = object_attribute_value_id
        self.__object_id = object_id
        self.__object_attribute_name = object_attribute_name
        self.__object_attribute_value = object_attribute_value

    @property
    def object_attribute_value_id(self):
        '''
        Get object attribute value id

        Parameters
        ----------
        None

        Returns
        -------
        str
            Object attribute value id
        
        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        return self.__object_attribute_value_id
    
    @property
    def object_id(self):
        '''
        Get object id

        Parameters
        ----------
        None

        Returns
        -------
        str
            Object id
        
        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        return self.__object_id
    
    @property
    def object_attribute_name(self):
        '''
        Get object attribute name

        Parameters
        ----------
        None

        Returns
        -------
        str
            Object attribute name
        
        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        return self.__object_attribute_name
    
    @property
    def object_attribute_value(self):
        '''
        Get object attribute value

        Parameters
        ----------
        None

        Returns
        -------
        str
            Object attribute value
        
        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        return self.__object_attribute_value
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_attribute_value_id already exists before execute create_object_attribute_value qualifier
            
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_attribute_value_id can be created
        if self.__object_attribute_value_id in current_state['object_attribute_value']:
            raise ValueError(f'{self.__object_attribute_value_id} must not be an existing object_attribute_value_id before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object_attribute_value'][self.__object_attribute_value_id] = {
            'name': self.__object_attribute_name,
            'value': self.__object_attribute_value,
            'existency': True,
            'object_id': self.__object_id
        }
        current_state['object'][self.__object_id]['object_attribute_value_ids'].append(self.__object_attribute_value_id)
        involved_ids['object_attribute_value'].add(self.__object_attribute_value_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object_attribute_value table of OCED model
        row = {
            'object_attribute_value_id': [self.__object_attribute_value_id], 
            'object_id': [self.__object_id], 
            'object_attribute_name': [self.__object_attribute_name], 
            'object_attribute_value': [self.__object_attribute_value], 
            'object_attribute_value_existency': [True]
        }
        OCED_model._OCED__object_attribute_value = pd.concat([OCED_model._OCED__object_attribute_value, pd.DataFrame(row)], ignore_index=True)
        # update object_attribute_name table of OCED model
        if self.__object_attribute_name not in OCED_model._OCED__object_attribute_name['object_attribute_name'].values:
            row = {
                'object_attribute_name': [self.__object_attribute_name]
            }
            OCED_model._OCED__object_attribute_name = pd.concat([OCED_model._OCED__object_attribute_name, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object_attribute_value table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter], 
            'object_attribute_value_id': [self.__object_attribute_value_id], 
            'qualifier_type': [self.qualifier_type], 
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_attribute_value = pd.concat([OCED_model._OCED__event_x_object_attribute_value, pd.DataFrame(row)], ignore_index=True)

    @override
    def __log(self):
        '''
        Get log create_object_attribute_value qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_attribute_value_id': self.__object_attribute_value_id,
                'object_id': self.__object_id,
                'object_attribute_name': self.__object_attribute_name,
                'object_attribute_value': self.__object_attribute_value
            }
        }


class delete_object(__Qualifier):
    '''
    Class to handle delete_object qualifiers

    Attributes
    ----------
    object_id : str
        Object id

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_id):
        '''
        Initialize delete_object qualifier

        Parameters
        ----------
        object_id : str
            Object id

        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_id is not a string

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_id
        if not isinstance(object_id, str):
            raise TypeError('object_id must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'DELETE')
        self.__object_id = object_id

    @property
    def object_id(self):
        '''
        Get object id

        Parameters
        ----------
        None

        Returns
        -------
        str
            Object id
        
        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        return self.__object_id
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
            
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_id does not exist before execute delete_object qualifier
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_id can be deleted
        if self.__object_id not in current_state['object'] or current_state['object'][self.__object_id]['existency'] == False:
            raise ValueError(f'{self.__object_id} must be an existing object_id before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object'][self.__object_id]['existency'] = False
        involved_ids['object'].add(self.__object_id)
        for object_relation_id in current_state['object'][self.__object_id]['object_relation_ids']:
            if current_state['object_relation'][object_relation_id]['existency'] == False:
                continue
            current_state['object_relation'][object_relation_id]['existency'] = False
            involved_ids['object_relation'].add(object_relation_id)
        for object_attribute_value_id in current_state['object'][self.__object_id]['object_attribute_value_ids']:
            if current_state['object_attribute_value'][object_attribute_value_id]['existency'] == False:
                continue
            current_state['object_attribute_value'][object_attribute_value_id]['existency'] = False
            involved_ids['object_attribute_value'].add(object_attribute_value_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object table of OCED model
        row = {
            'object_id': [self.__object_id], 
            'object_type': OCED_model._OCED__current_state['object'][self.__object_id]['type'],
            'object_existency': [False]
        }
        OCED_model._OCED__object = pd.concat([OCED_model._OCED__object, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter], 
            'object_id': [self.__object_id], 
            'qualifier_type': [self.qualifier_type], 
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object = pd.concat([OCED_model._OCED__event_x_object, pd.DataFrame(row)], ignore_index=True)
        # update object_relation and event_x_object_relation table of OCED model
        for object_relation_id in OCED_model._OCED__current_state['object'][self.__object_id]['object_relation_ids']:
            if OCED_model._OCED__current_state['object_relation'][object_relation_id]['existency'] == False:
                continue
            # update object_relation table of OCED model
            row = {
                'object_relation_id': [object_relation_id], 
                'from_object_id': [OCED_model._OCED__current_state['object_relation'][object_relation_id]['from_object_id']], 
                'to_object_id': [OCED_model._OCED__current_state['object_relation'][object_relation_id]['to_object_id']], 
                'object_relation_type': [OCED_model._OCED__current_state['object_relation'][object_relation_id]['type']], 
                'object_relation_existency': [False]
            }
            OCED_model._OCED__object_relation = pd.concat([OCED_model._OCED__object_relation, pd.DataFrame(row)], ignore_index=True)
            # update event_x_object_relation table of OCED model
            row = {
                'event_id': [OCED_model._OCED__event_counter], 
                'object_relation_id': [object_relation_id], 
                'qualifier_type': [self.qualifier_type], 
                'qualifier_index': [qualifier_index]
            }
            OCED_model._OCED__event_x_object_relation = pd.concat([OCED_model._OCED__event_x_object_relation, pd.DataFrame(row)], ignore_index=True)
        # update object_attribute_value and event_x_object_attribute_value table of OCED model
        for object_attribute_value_id in OCED_model._OCED__current_state['object'][self.__object_id]['object_attribute_value_ids']:
            if OCED_model._OCED__current_state['object_attribute_value'][object_attribute_value_id]['existency'] == False:
                continue
            # update object_attribute_value table of OCED model
            row = {
                'object_attribute_value_id': [object_attribute_value_id], 
                'object_id': [OCED_model._OCED__current_state['object_attribute_value'][object_attribute_value_id]['object_id']], 
                'object_attribute_name': [OCED_model._OCED__current_state['object_attribute_value'][object_attribute_value_id]['name']], 
                'object_attribute_value': [OCED_model._OCED__current_state['object_attribute_value'][object_attribute_value_id]['value']], 
                'object_attribute_value_existency': [False]
            }
            OCED_model._OCED__object_attribute_value = pd.concat([OCED_model._OCED__object_attribute_value, pd.DataFrame(row)], ignore_index=True)
            # update event_x_object_attribute_value table of OCED model
            row = {
                'event_id': [OCED_model._OCED__event_counter], 
                'object_attribute_value_id': [object_attribute_value_id], 
                'qualifier_type': [self.qualifier_type], 
                'qualifier_index': [qualifier_index]
            }
            OCED_model._OCED__event_x_object_attribute_value = pd.concat([OCED_model._OCED__event_x_object_attribute_value, pd.DataFrame(row)], ignore_index=True)

    @override
    def __log(self):
        '''
        Get log delete_object qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_id': self.__object_id
            }
        }


class delete_object_relation(__Qualifier):
    '''
    Class to handle delete_object_relation qualifiers

    Attributes
    ----------
    object_relation_id : str
        Object relation id

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_relation_id):
        '''
        Initialize delete_object_relation qualifier

        Parameters
        ----------
        object_relation_id : str
            Object relation id

        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_relation_id is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_relation_id
        if not isinstance(object_relation_id, str):
            raise TypeError('object_relation_id must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'DELETE')
        self.__object_relation_id = object_relation_id

    @property
    def object_relation_id(self):
        '''
        Get object relation id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object relation id
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_relation_id
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_relation_id does not exist before execute delete_object_relation qualifier
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_relation_id can be deleted
        if self.__object_relation_id not in current_state['object_relation'] or current_state['object_relation'][self.__object_relation_id]['existency'] == False:
            raise ValueError(f'{self.__object_relation_id} must be an existing object_relation_id before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object_relation'][self.__object_relation_id]['existency'] = False
        involved_ids['object_relation'].add(self.__object_relation_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object_relation table of OCED model
        row = {
            'object_relation_id': [self.__object_relation_id],
            'from_object_id': [OCED_model._OCED__current_state['object_relation'][self.__object_relation_id]['from_object_id']],
            'to_object_id': [OCED_model._OCED__current_state['object_relation'][self.__object_relation_id]['to_object_id']],
            'object_relation_type': [OCED_model._OCED__current_state['object_relation'][self.__object_relation_id]['type']],
            'object_relation_existency': [False]
        }
        OCED_model._OCED__object_relation = pd.concat([OCED_model._OCED__object_relation, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object_relation table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_relation_id': [self.__object_relation_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_relation = pd.concat([OCED_model._OCED__event_x_object_relation, pd.DataFrame(row)], ignore_index=True)

    @override
    def __log(self):
        '''
        Get log delete_object_relation qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_relation_id': self.__object_relation_id
            }
        }


class delete_object_attribute_value(__Qualifier):
    '''
    Class to handle delete_object_attribute_value qualifiers

    Attributes
    ----------
    object_attribute_value_id : str
        Object attribute value id

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_attribute_value_id):
        '''
        Initialize delete_object_attribute_value qualifier

        Parameters
        ----------
        object_attribute_value_id : str
            Object attribute value id
        
        Returns
        -------
        None
        
        Raises
        ------
        TypeError
            - If object_attribute_value_id is not a string
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check object_attribute_value_id
        if not isinstance(object_attribute_value_id, str):
            raise TypeError('object_attribute_value_id must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'DELETE')
        self.__object_attribute_value_id = object_attribute_value_id

    @property
    def object_attribute_value_id(self):
        '''
        Get object attribute value id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object attribute value id
        
        Raises
        ------
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_attribute_value_id
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED

        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        ValueError
            - If object_attribute_value_id does not exist before execute delete_object_attribute_value qualifier
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check if object_attribute_value_id can be deleted
        if self.__object_attribute_value_id not in current_state['object_attribute_value'] or current_state['object_attribute_value'][self.__object_attribute_value_id]['existency'] == False:
            raise ValueError(f'{self.__object_attribute_value_id} must be an existing object_attribute_value_id before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object_attribute_value'][self.__object_attribute_value_id]['existency'] = False
        involved_ids['object_attribute_value'].add(self.__object_attribute_value_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object_attribute_value table of OCED model
        row = {
            'object_attribute_value_id': [self.__object_attribute_value_id],
            'object_id': [OCED_model._OCED__current_state['object_attribute_value'][self.__object_attribute_value_id]['object_id']],
            'object_attribute_name': [OCED_model._OCED__current_state['object_attribute_value'][self.__object_attribute_value_id]['name']],
            'object_attribute_value': [OCED_model._OCED__current_state['object_attribute_value'][self.__object_attribute_value_id]['value']],
            'object_attribute_value_existency': [False]
        }
        OCED_model._OCED__object_attribute_value = pd.concat([OCED_model._OCED__object_attribute_value, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object_attribute_value table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_attribute_value_id': [self.__object_attribute_value_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_attribute_value = pd.concat([OCED_model._OCED__event_x_object_attribute_value, pd.DataFrame(row)], ignore_index=True)
    
    @override
    def __log(self):
        '''
        Get log delete_object_attribute_value qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_attribute_value_id': self.__object_attribute_value_id
            }
        }
    

class modify_object(__Qualifier):
    '''
    Class to handle modify_object qualifiers

    Attributes
    ----------
    object_id : str
        Object id
    new_object_type : str
        New object type

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_id, new_object_type):
        '''
        Initialize modify_object qualifier

        Parameters
        ----------
        object_id : str
            Object id
        new_object_type : str
            New object type
        
        Returns
        -------
        None
        
        Raises
        ------
        TypeError
            - If object_id is not a string
            - If new_object_type is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_id
        if not isinstance(object_id, str):
            raise TypeError('object_id must be a string')
        # check new_object_type
        if not isinstance(new_object_type, str):
            raise TypeError('new_object_type must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'MODIFY')
        self.__object_id = object_id
        self.__new_object_type = new_object_type

    @property
    def object_id(self):
        '''
        Get object id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_id
    
    @property
    def new_object_type(self):
        '''
        Get new object type

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            New object type
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__new_object_type
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
            
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_id does not exist before execute modify_object qualifier
            - If new_object_type is equal to current object_type of object_id before execute modify_object qualifier
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_id can be modified
        if self.__object_id not in current_state['object'] or current_state['object'][self.__object_id]['existency'] == False:
            raise ValueError(f'{self.__object_id} must be an existing object_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if current_state['object'][self.__object_id]['type'] == self.__new_object_type:
            raise ValueError(f'{self.__new_object_type} must be different from current object_type of {self.__object_id} before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object'][self.__object_id]['type'] = self.__new_object_type
        involved_ids['object'].add(self.__object_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object table of OCED model
        row = {
            'object_id': [self.__object_id],
            'object_type': [self.__new_object_type],
            'object_existency': [True]
        }
        OCED_model._OCED__object = pd.concat([OCED_model._OCED__object, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_id': [self.__object_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object = pd.concat([OCED_model._OCED__event_x_object, pd.DataFrame(row)], ignore_index=True)
    
    @override
    def __log(self):
        '''
        Get log modify_object qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_id': self.__object_id,
                'new_object_type': self.__new_object_type
            }
        }
    

class modify_object_relation(__Qualifier):
    '''
    Class to handle modify_object_relation qualifiers

    Attributes
    ----------
    object_relation_id : str
        Object relation id
    new_object_relation_type : str
        New object relation type

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_relation_id, new_object_relation_type):
        '''
        Initialize modify_object_relation qualifier

        Parameters
        ----------
        object_relation_id : str
            Object relation id
        new_object_relation_type : str
            New object relation type
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_relation_id is not a string
            - If new_object_relation_type is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_relation_id
        if not isinstance(object_relation_id, str):
            raise TypeError('object_relation_id must be a string')
        # check new_relation_type
        if not isinstance(new_object_relation_type, str):
            raise TypeError('new_object_relation_type must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'MODIFY')
        self.__object_relation_id = object_relation_id
        self.__new_object_relation_type = new_object_relation_type

    @property
    def object_relation_id(self):
        '''
        Get object relation id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object relation id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_relation_id
    
    @property
    def new_object_relation_type(self):
        '''
        Get new object relation type

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            New object relation type
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__new_object_relation_type
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
            
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_relation_id does not exist before execute modify_object_relation qualifier
            - If new_object_relation_type is equal to current object_relation_type of object_relation_id before execute modify_object_relation qualifier
            
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_relation_id can be modified
        if self.__object_relation_id not in current_state['object_relation'] or current_state['object_relation'][self.__object_relation_id]['existency'] == False:
            raise ValueError(f'{self.__object_relation_id} must be an existing object_relation_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if current_state['object_relation'][self.__object_relation_id]['type'] == self.__new_object_relation_type:
            raise ValueError(f'{self.__new_object_relation_type} must be different from current object_relation_type of {self.__object_relation_id} before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object_relation'][self.__object_relation_id]['type'] = self.__new_object_relation_type
        involved_ids['object_relation'].add(self.__object_relation_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object_relation table of OCED model
        row = {
            'object_relation_id': [self.__object_relation_id],
            'from_object_id': [OCED_model._OCED__current_state['object_relation'][self.__object_relation_id]['from_object_id']],
            'to_object_id': [OCED_model._OCED__current_state['object_relation'][self.__object_relation_id]['to_object_id']],
            'object_relation_type': [self.__new_object_relation_type],
            'object_relation_existency': [True]
        }
        OCED_model._OCED__object_relation = pd.concat([OCED_model._OCED__object_relation, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object_relation table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_relation_id': [self.__object_relation_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_relation = pd.concat([OCED_model._OCED__event_x_object_relation, pd.DataFrame(row)], ignore_index=True)

    @override
    def __log(self):
        '''
        Get log modify_object_relation qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_relation_id': self.__object_relation_id,
                'new_object_relation_type': self.new_object_relation_type
            }
        }


class modify_object_attribute_value(__Qualifier):
    '''
    Class to handle modify_object_attribute_value qualifiers

    Attributes
    ----------
    object_attribute_value_id : str
        Object attribute value id
    new_object_attribute_value : str
        New object attribute value

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_attribute_value_id, new_object_attribute_value):
        '''
        Initialize modify_object_attribute_value qualifier

        Parameters
        ----------
        object_attribute_value_id : str
            Object attribute value id
        new_object_attribute_value : str
            New object attribute value
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_attribute_value_id is not a string
            - If new_object_attribute_value is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_attribute_value_id
        if not isinstance(object_attribute_value_id, str):
            raise TypeError('object_attribute_value_id must be a string')
        # check new_object_attribute_value
        if not isinstance(new_object_attribute_value, str):
            raise TypeError('new_object_attribute_value must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'MODIFY')
        self.__object_attribute_value_id = object_attribute_value_id
        self.__new_object_attribute_value = new_object_attribute_value

    @property
    def object_attribute_value_id(self):
        '''
        Get object attribute value id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object attribute value id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_attribute_value_id
    
    @property
    def new_object_attribute_value(self):
        '''
        Get new object attribute value

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            New object attribute value
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__new_object_attribute_value
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_attribute_value_id does not exist before execute modify_object_attribute_value qualifier
            - If new_object_attribute_value is equal to current object_attribute_value of object_attribute_value_id before execute modify_object_attribute_value qualifier
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_attribute_value_id can be modified
        if self.__object_attribute_value_id not in current_state['object_attribute_value'] or current_state['object_attribute_value'][self.__object_attribute_value_id]['existency'] == False:
            raise ValueError(f'{self.__object_attribute_value_id} must be an existing object_attribute_value_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if current_state['object_attribute_value'][self.__object_attribute_value_id]['value'] == self.__new_object_attribute_value:
            raise ValueError(f'{self.__new_object_attribute_value} must be different from current object_attribute_value of {self.__object_attribute_value_id} before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        current_state['object_attribute_value'][self.__object_attribute_value_id]['value'] = self.__new_object_attribute_value
        involved_ids['object_attribute_value'].add(self.__object_attribute_value_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update object_attribute_value table of OCED model
        row = {
            'object_attribute_value_id': [self.__object_attribute_value_id],
            'object_id': [OCED_model._OCED__current_state['object_attribute_value'][self.__object_attribute_value_id]['object_id']],
            'object_attribute_name': [OCED_model._OCED__current_state['object_attribute_value'][self.__object_attribute_value_id]['name']],
            'object_attribute_value': [self.__new_object_attribute_value],
            'object_attribute_value_existency': [True]
        }
        OCED_model._OCED__object_attribute_value = pd.concat([OCED_model._OCED__object_attribute_value, pd.DataFrame(row)], ignore_index=True)
        # update event_x_object_attribute_value table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_attribute_value_id': [self.__object_attribute_value_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_attribute_value = pd.concat([OCED_model._OCED__event_x_object_attribute_value, pd.DataFrame(row)], ignore_index=True)
    
    @override
    def __log(self):
        '''
        Get log modify_object_attribute_value qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_attribute_value_id': self.__object_attribute_value_id,
                'new_object_attribute_value': self.__new_object_attribute_value
            }
        }
    

class involve_object(__Qualifier):
    '''
    Class to handle involve_object qualifiers

    Attributes
    ----------
    object_id : str
        Object id

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_id):
        '''
        Initialize involve_object qualifier

        Parameters
        ----------
        object_id : str
            Object id
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_id is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_id
        if not isinstance(object_id, str):
            raise TypeError('object_id must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'INVOLVE')
        self.__object_id = object_id

    @property
    def object_id(self):
        '''
        Get object id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_id
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_id does not exist before execute involve_object qualifier
            - If object_id is already involved before execute involve_object qualifier
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_id can be involved
        if self.__object_id not in current_state['object'] or current_state['object'][self.__object_id]['existency'] == False:
            raise ValueError(f'{self.__object_id} must be an existing object_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if self.__object_id in involved_ids['object']:
            raise ValueError(f'{self.__object_id} must not be involved before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        involved_ids['object'].add(self.__object_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update event_x_object table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_id': [self.__object_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object = pd.concat([OCED_model._OCED__event_x_object, pd.DataFrame(row)], ignore_index=True)
    
    @override
    def __log(self):
        '''
        Get log involve_object qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_id': self.__object_id
            }
        }


class involve_object_relation(__Qualifier):
    '''
    Class to handle involve_object_relation qualifiers

    Attributes
    ----------
    object_relation_id : str
        Object relation id

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_relation_id):
        '''
        Initialize involve_object_relation qualifier

        Parameters
        ----------
        object_relation_id : str
            Object relation id
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_relation_id is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_relation_id
        if not isinstance(object_relation_id, str):
            raise TypeError('object_relation_id must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'INVOLVE')
        self.__object_relation_id = object_relation_id

    @property
    def object_relation_id(self):
        '''
        Get object relation id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object relation id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_relation_id
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED
        
        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_relation_id does not exist before execute involve_object_relation qualifier
            - If object_relation_id is already involved before execute involve_object_relation qualifier
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_relation_id can be involved
        if self.__object_relation_id not in current_state['object_relation'] or current_state['object_relation'][self.__object_relation_id]['existency'] == False:
            raise ValueError(f'{self.__object_relation_id} must be an existing object_relation_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if self.__object_relation_id in involved_ids['object_relation']:
            raise ValueError(f'{self.__object_relation_id} must not be involved before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        involved_ids['object_relation'].add(self.__object_relation_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # execute event_x_object_relation table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_relation_id': [self.__object_relation_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_relation = pd.concat([OCED_model._OCED__event_x_object_relation, pd.DataFrame(row)], ignore_index=True)

    @override
    def __log(self):
        '''
        Get log involve_object_relation qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_relation_id': self.__object_relation_id
            }
        }


class involve_object_attribute_value(__Qualifier):
    '''
    Class to handle involve_object_attribute_value qualifiers

    Attributes
    ----------
    object_attribute_value_id : str
        Object attribute value id

    Methods
    -------
    None

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, object_attribute_value_id):
        '''
        Initialize involve_object_attribute_value qualifier

        Parameters
        ----------
        object_attribute_value_id : str
            Object attribute value id
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If object_attribute_value_id is not a string
        
        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check object_attribute_value_id
        if not isinstance(object_attribute_value_id, str):
            raise TypeError('object_attribute_value_id must be a string')
        # initialize
        super().__init__(self.__class__.__name__, 'INVOLVE')
        self.__object_attribute_value_id = object_attribute_value_id

    @property
    def object_attribute_value_id(self):
        '''
        Get object attribute value id

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Object attribute value id
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_attribute_value_id
    
    @override
    def __update_current_state(self, current_state, involved_ids, qualifier_index):
        '''
        Update current state of OCED

        Parameters
        ----------
        current_state : dict
            Dictionary with current state of OCED
        involved_ids : dict
            Dictionary with involved ids of OCED
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If object_attribute_value_id does not exist before execute involve_object_attribute_value qualifier
            - If object_attribute_value_id is already involved before execute involve_object_attribute_value qualifier
            
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check if object_attribute_value_id can be involved
        if self.__object_attribute_value_id not in current_state['object_attribute_value'] or current_state['object_attribute_value'][self.__object_attribute_value_id]['existency'] == False:
            raise ValueError(f'{self.__object_attribute_value_id} must be an existing object_attribute_value_id before execute {self.__name__} qualifier at index {qualifier_index}')
        if self.__object_attribute_value_id in involved_ids['object_attribute_value']:
            raise ValueError(f'{self.__object_attribute_value_id} must not be involved before execute {self.__name__} qualifier at index {qualifier_index}')
        # update current state of OCED model and involved ids in the current event
        involved_ids['object_attribute_value'].add(self.__object_attribute_value_id)

    @override
    def __update_tables(self, OCED_model, qualifier_index):
        '''
        Update tables of OCED model
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        qualifier_index : int
            Qualifier index
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # execute event_x_object_attribute_value table of OCED model
        row = {
            'event_id': [OCED_model._OCED__event_counter],
            'object_attribute_value_id': [self.__object_attribute_value_id],
            'qualifier_type': [self.qualifier_type],
            'qualifier_index': [qualifier_index]
        }
        OCED_model._OCED__event_x_object_attribute_value = pd.concat([OCED_model._OCED__event_x_object_attribute_value, pd.DataFrame(row)], ignore_index=True)
    
    @override
    def __log(self):
        '''
        Get log involve_object_attribute_value qualifier
        
        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with qualifier and arguments
            
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return {
            'qualifier': self.qualifier_name,
            'arguments': {
                'object_attribute_value_id': self.__object_attribute_value_id
            }
        }


class Event:
    '''
    Class to handle events

    Attributes
    ----------
    event_time : str ISO 8601-1:2019
        Event time
    event_type : str
        Event type
    qualifiers : list
        List of qualifiers
    event_attributes : dict -> str : str
        Event attributes

    Methods
    -------
    None
    
    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self, event_time, event_type, qualifiers=[], event_attributes={}):
        '''
        Initialize Event object

        Parameters
        ----------
        event_time : str ISO 8601-1:2019
            Event time
        event_type : str
            Event type
        qualifiers : list
            List of qualifiers (default is empty list)  
        event_attributes : dict -> str : str
            Event attributes (default is empty dictionary)
        
        Returns
        -------
        None

        Raises
        ------
        TypeError
            - If event_time is not a string ISO 8601-1:2019
            - If event_type is not a string
            - If qualifiers is not a list of qualifiers
            - If event_attributes is not a dictionary of string : string

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # check event_time
        try:
            event_time = datetime.fromtimestamp(datetime.fromisoformat(event_time).timestamp()).isoformat()
        except:
            raise TypeError('time must be a valid ISO 8601-1:2019 string')
        # check event_id
        if not isinstance(event_type, str):
            raise TypeError('event_type must be a string')
        # check qualifiers
        if not isinstance(qualifiers, list):
            raise TypeError('qualifiers must be a list of qualifiers')
        types = [create_object, create_object_relation, create_object_attribute_value, delete_object, delete_object_relation, delete_object_attribute_value, modify_object, modify_object_relation, modify_object_attribute_value, involve_object, involve_object_relation, involve_object_attribute_value]
        for elem in qualifiers:
            if not type(elem) in types:
                raise TypeError('qualifiers must be a list of qualifiers')
        # check event_attributes
        if not isinstance(event_attributes, dict):
            raise TypeError('event_attributes must be a dictionary of string : string')
        for name, value in event_attributes.items():
            if not isinstance(name, str) or not isinstance(value, str):
                raise TypeError('event_attributes must be a dictionary of string : string')
        # initialize
        self.__event_time = event_time
        self.__event_type = event_type
        self.__qualifiers = qualifiers
        self.__event_attributes = event_attributes
        return

    @property
    def event_time(self):
        '''
        Get event_time

        Parameters
        ----------
        None
        
        Returns
        -------
        str ISO 8601-1:2019
            Event time
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_time
    
    @property
    def event_type(self):
        '''
        Get event type

        Parameters
        ----------
        None
        
        Returns
        -------
        str
            Event type
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_type
    
    @property
    def qualifiers(self):
        '''
        Get list of qualifiers

        Parameters
        ----------
        None
        
        Returns
        -------
        list
            List of qualifiers
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__qualifiers
    
    @property
    def event_attributes(self):
        '''
        Get event attributes

        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary of event attributes
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_attributes

    def __precondition(self, OCED_model):
        '''
        Check if event can be executed
        
        Parameters
        ----------
        OCED_model : OCED
            OCED model
        
        Returns
        -------
        None
        
        Raises
        ------
        ValueError
            - If event_time is not greater than last event time
            - If a qualifier cannot be executed

        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check event_time
        max_time = OCED_model._OCED__event_time['event_time'].max()
        if isinstance(max_time, str) and max_time >= self.__event_time:
            raise ValueError('Event time must be greater than last event time')
        # check if qualifiers can be executed
        current_state = deepcopy(OCED_model._OCED__current_state)
        involved_ids = {'object': set(), 'object_relation': set(), 'object_attribute_value': set()}
        for qualifier_index, qualifier in enumerate(self.__qualifiers):
            if qualifier.qualifier_name == 'create_object':
                qualifier._create_object__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'create_object_relation':
                qualifier._create_object_relation__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'create_object_attribute_value':
                qualifier._create_object_attribute_value__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'delete_object':
                qualifier._delete_object__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'delete_object_relation':
                qualifier._delete_object_relation__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'delete_object_attribute_value':
                qualifier._delete_object_attribute_value__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'modify_object':
                qualifier._modify_object__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'modify_object_relation':
                qualifier._modify_object_relation__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'modify_object_attribute_value':
                qualifier._modify_object_attribute_value__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'involve_object':
                qualifier._involve_object__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'involve_object_relation':
                qualifier._involve_object_relation__update_current_state(current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'involve_object_attribute_value':
                qualifier._involve_object_attribute_value__update_current_state(current_state, involved_ids, qualifier_index)
    
    def __execute(self, OCED_model):
        '''
        Execute event

        Parameters
        ----------
        OCED_model : OCED
            OCED model
        
        Returns
        -------
        None
        
        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # update event table in OCED_model
        row = {'event_id': [OCED_model._OCED__event_counter], 'event_type': [self.__event_type], 'event_time': [self.__event_time]}
        OCED_model._OCED__event = pd.concat([OCED_model._OCED__event, pd.DataFrame(row)], ignore_index=True)
        # update event_type table in OCED_model
        if not self.__event_type in OCED_model._OCED__event_type['event_type'].values:
            row = {'event_type': [self.__event_type]}
            OCED_model._OCED__event_type = pd.concat([OCED_model._OCED__event_type, pd.DataFrame(row)], ignore_index=True)
        # update event_time table in OCED_model
        row = {'event_time': [self.__event_time]}
        OCED_model._OCED__event_time = pd.concat([OCED_model._OCED__event_time, pd.DataFrame(row)], ignore_index=True)
        # update event_attribute_name table in OCED_model
        rows = {'event_attribute_name': []}
        existing_event_attribute_names = OCED_model._OCED__event_attribute_name['event_attribute_name'].values
        for event_attribute_name in self.__event_attributes.keys():
            if not event_attribute_name in existing_event_attribute_names:
                rows['event_attribute_name'].append(event_attribute_name)
        OCED_model._OCED__event_attribute_name = pd.concat([OCED_model._OCED__event_attribute_name, pd.DataFrame(rows)], ignore_index=True)
        # update event_attribute_value table in OCED_model
        rows = {'event_id': [], 'event_attribute_name': [], 'event_attribute_value': []}
        for event_attribute_name, event_attribute_value in self.__event_attributes.items():
            rows['event_id'].append(OCED_model._OCED__event_counter)
            rows['event_attribute_name'].append(event_attribute_name)
            rows['event_attribute_value'].append(event_attribute_value)
        OCED_model._OCED__event_attribute_value = pd.concat([OCED_model._OCED__event_attribute_value, pd.DataFrame(rows)], ignore_index=True)
        # execute qualifiers
        involved_ids = {'object': set(), 'object_relation': set(), 'object_attribute_value': set()}
        for qualifier_index, qualifier in enumerate(self.__qualifiers):
            if qualifier.qualifier_name == 'create_object':
                qualifier._create_object__update_tables(OCED_model, qualifier_index)
                qualifier._create_object__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'create_object_relation':
                qualifier._create_object_relation__update_tables(OCED_model, qualifier_index)
                qualifier._create_object_relation__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'create_object_attribute_value':
                qualifier._create_object_attribute_value__update_tables(OCED_model, qualifier_index)
                qualifier._create_object_attribute_value__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'delete_object':
                qualifier._delete_object__update_tables(OCED_model, qualifier_index)
                qualifier._delete_object__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'delete_object_relation':
                qualifier._delete_object_relation__update_tables(OCED_model, qualifier_index)
                qualifier._delete_object_relation__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'delete_object_attribute_value':
                qualifier._delete_object_attribute_value__update_tables(OCED_model, qualifier_index)
                qualifier._delete_object_attribute_value__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'modify_object':
                qualifier._modify_object__update_tables(OCED_model, qualifier_index)
                qualifier._modify_object__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'modify_object_relation':
                qualifier._modify_object_relation__update_tables(OCED_model, qualifier_index)
                qualifier._modify_object_relation__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'modify_object_attribute_value':
                qualifier._modify_object_attribute_value__update_tables(OCED_model, qualifier_index)
                qualifier._modify_object_attribute_value__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'involve_object':
                qualifier._involve_object__update_tables(OCED_model, qualifier_index)
                qualifier._involve_object__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'involve_object_relation':
                qualifier._involve_object_relation__update_tables(OCED_model, qualifier_index)
                qualifier._involve_object_relation__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)
            elif qualifier.qualifier_name == 'involve_object_attribute_value':
                qualifier._involve_object_attribute_value__update_tables(OCED_model, qualifier_index)
                qualifier._involve_object_attribute_value__update_current_state(OCED_model._OCED__current_state, involved_ids, qualifier_index)

    def __log(self, OCED_model):
        '''
        Log event

        Parameters
        ----------
        OCED_model : OCED
            OCED model
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        log = []
        for qualifier in self.__qualifiers:
            if qualifier.qualifier_name == 'create_object':
                log.append(qualifier._create_object__log())
            elif qualifier.qualifier_name == 'create_object_relation':
                log.append(qualifier._create_object_relation__log())
            elif qualifier.qualifier_name == 'create_object_attribute_value':
                log.append(qualifier._create_object_attribute_value__log())
            elif qualifier.qualifier_name == 'delete_object':
                log.append(qualifier._delete_object__log())
            elif qualifier.qualifier_name == 'delete_object_relation':
                log.append(qualifier._delete_object_relation__log())
            elif qualifier.qualifier_name == 'delete_object_attribute_value':
                log.append(qualifier._delete_object_attribute_value__log())
            elif qualifier.qualifier_name == 'modify_object':
                log.append(qualifier._modify_object__log())
            elif qualifier.qualifier_name == 'modify_object_relation':
                log.append(qualifier._modify_object_relation__log())
            elif qualifier.qualifier_name == 'modify_object_attribute_value':
                log.append(qualifier._modify_object_attribute_value__log())
            elif qualifier.qualifier_name == 'involve_object':
                log.append(qualifier._involve_object__log())
            elif qualifier.qualifier_name == 'involve_object_relation':
                log.append(qualifier._involve_object_relation__log())
            elif qualifier.qualifier_name == 'involve_object_attribute_value':
                log.append(qualifier._involve_object_attribute_value__log())
        OCED_model._OCED__log[OCED_model._OCED__event_counter] = log


class OCED:
    '''
    Object-Centric Event Data

    Attributes
    ----------
    event : pandas.DataFrame
        DataFrame with events 

        | event_id | event_time | event_type |
        primary key: event_id
        foreign key: event_type references event_type.name
        foreign key: event_time references event_time.value

    event_type : pandas.DataFrame
        DataFrame with event types

        | event_type |
        primary key: event_type

    event_time : pandas.DataFrame
        DataFrame with event times

        | event_time |
        primary key: event_time

    event_attribute_name : pandas.DataFrame
        DataFrame with event attribute names

        | event_attribute_name |
        primary key: event_attribute_name

    event_attribute_value : pandas.DataFrame
        DataFrame with event attribute values

        | event_id | event_attribute_name | event_attribute_value |
        primary key: (event_id, event_attribute_name)
        foreign key: event_id references event.event_id
        foreign key: event_attribute_name references event_attribute_name.event_attribute_name

    object : pandas.DataFrame
        DataFrame with objects

        | object_id | object_type | object_existency |
        primary key: object_id
        foreign key: object_type references object_type.object_type

    object_type : pandas.DataFrame
        DataFrame with object types
        
        | object_type |
        primary key: object_type

    object_attribute_name : pandas.DataFrame
        DataFrame with object attribute names

        | object_attribute_name |
        primary key: object_attribute_name

    object_attribute_value : pandas.DataFrame
        DataFrame with object attribute values

        | object_attribute_value_id | object_id | object_attribute_name | object_attribute_value | object_attribute_value_existency |
        primary key: object_attribute_value_id
        foreign key: object_id references object.object_id
        foreign key: name references object_attribute_name.object_attribute_name

    object_relation : pandas.DataFrame
        DataFrame with object relations

        | object_relation_id | from_object_id | to_object_id | object_relation_type | object_relation_existency |
        primary key: object_relation_id
        foreign key: from_object_id references object.object_id
        foreign key: to_object_id references object.object_id
        foreign key: object_relation_type references object_relation_type.object_relation_type

    object_relation_type : pandas.DataFrame
        DataFrame with object relation types

        | object_relation_type |
        primary key: object_relation_type

    event_x_object : pandas.DataFrame
        DataFrame with events x objects

        | event_id | object_id | qualifier_type | qualifier_index |
        primary key: (event_id, object_id, qualifier_index)
        foreign key: event_id references event.event_id
        foreign key: object_id references object.object_id

    event_x_object_attribute_value : pandas.DataFrame
        DataFrame with events x object attribute values

        | event_id | object_attribute_value_id | qualifier_type | qualifier_index |
        primary key: (event_id, object_attribute_value_id, qualifier_index)
        foreign key: event_id references event.event_id
        foreign key: object_attribute_value_id references object_attribute_value.object_attribute_value_id

    event_x_object_relation : pandas.DataFrame
        DataFrame with events x object relations

        | event_id | object_relation_id | qualifier_type | qualifier_index |
        primary key: (event_id, object_relation_id, qualifier_index)
        foreign key: event_id references event.event_id
        foreign key: object_relation_id references object_relation.object_relation_id

    log : list
        List with events logs
    
            {
            
                'event_id1' : [
                
                    {
                    
                        'qualifier' : qualifier name,

                        'arguments' : {
                        
                            'argument1': value,

                            ...

                        }

                    },

                    ...

                ],

                ...

            }

    current_state : dict
        Dictionary with current state of OCED

            {
                
                'object': {
                
                    'object_id1': {
                    
                        'type': object type,

                        'existency': object existency,

                        'object_relation_ids': list of object relation ids (from_object_id or to_object_id),

                        'object_attribute_value_ids': list of object attribute value ids (object_id),

                    },

                    ...

                },

                'object_attribute_value': {
                
                    'object_attribute_value_id1': {
                    
                        'object_id': object id,

                        'name': object attribute name,

                        'value': object attribute value,

                        'existency': object attribute value existency,

                    },

                    ...

                },

                'object_relation': {
                
                    'object_relation_id1': {
                    
                        'from_object_id': from object id,

                        'to_object_id': to object id,

                        'type': object relation type,

                        'existency': object relation existency

                    },

                    ...

                }

            }

    event_counter : int
        Event counter

    Methods
    -------
    insert_event(event)
        Insert an event

    Notes
    -----
    None

    Examples
    --------
    None
    '''

    def __init__(self):
        '''
        Initialize OCED object

        Parameters
        ----------
        None
        
        Returns
        -------
        None

        Raises
        ------
        None

        Notes
        -----
        None

        Examples
        --------
        None
        '''
        # initialize
        self.__event = pd.DataFrame(columns=['event_id', 'event_type', 'event_time'])
        self.__event_type = pd.DataFrame(columns=['event_type'])
        self.__event_time = pd.DataFrame(columns=['event_time'])
        self.__event_attribute_name = pd.DataFrame(columns=['event_attribute_name'])
        self.__event_attribute_value = pd.DataFrame(columns=['event_id', 'event_attribute_name', 'event_attribute_value'])
        self.__object = pd.DataFrame(columns=['object_id', 'object_type', 'object_existency'])
        self.__object_type = pd.DataFrame(columns=['object_type'])
        self.__object_attribute_name = pd.DataFrame(columns=['object_attribute_name'])
        self.__object_attribute_value = pd.DataFrame(columns=['object_attribute_value_id', 'object_id', 'object_attribute_name', 'object_attribute_value', 'object_attribute_value_existency'])
        self.__object_relation = pd.DataFrame(columns=['object_relation_id', 'from_object_id', 'to_object_id', 'object_relation_type', 'object_relation_existency'])
        self.__object_relation_type = pd.DataFrame(columns=['object_relation_type'])
        self.__event_x_object = pd.DataFrame(columns=['event_id', 'object_id', 'qualifier_type', 'qualifier_index'])
        self.__event_x_object_attribute_value = pd.DataFrame(columns=['event_id', 'object_attribute_value_id', 'qualifier_type', 'qualifier_index'])
        self.__event_x_object_relation = pd.DataFrame(columns=['event_id', 'object_relation_id', 'qualifier_type', 'qualifier_index'])
        self.__log = {}
        self.__current_state = {
            'object': {},
            'object_relation': {},
            'object_attribute_value': {}
        }
        self.__event_counter = 0
    
    def insert_event(self, event):
        '''
        Insert an event
        
        Parameters
        ----------
        event : Event
            Event object
        
        Returns
        -------
        None
        
        Raises
        ------
        TypeError
            - If event is not an Event object
        ValueError
            - If event does not satisfy the precondition (see Event.__precondition)
            
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # check event
        if not isinstance(event, Event):
            raise TypeError('event must be an Event object')
        # check if event can be executed
        event._Event__precondition(self)
        # execute event
        event._Event__execute(self)
        # log event
        event._Event__log(self)
        # update event_counter
        self.__event_counter += 1

    @property
    def event(self):
        '''
        Get events

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with events
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event
    
    @property
    def event_type(self):
        '''
        Get event types

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with event types
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_type
    
    @property
    def event_time(self):
        '''
        Get event times

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with event times
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_time
    
    @property
    def event_attribute_name(self):
        '''
        Get event attribute names

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with event attribute names
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_attribute_name
    
    @property
    def event_attribute_value(self):
        '''
        Get event attribute values

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with event attribute values
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_attribute_value
    
    @property
    def object(self):
        '''
        Get objects

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with objects
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object
    
    @property
    def object_type(self):
        '''
        Get object types

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with object types
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_type
    
    @property
    def object_attribute_name(self):
        '''
        Get object attribute names

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with object attribute names
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_attribute_name
    
    @property
    def object_attribute_value(self):
        '''
        Get object attribute values

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with object attribute values
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_attribute_value
    
    @property
    def object_relation(self):
        '''
        Get object relations

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with object relations
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_relation
    
    @property
    def object_relation_type(self):
        '''
        Get object relation types

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with object relation types
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__object_relation_type
    
    @property
    def event_x_object(self):
        '''
        Get events x objects

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with events x objects
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_x_object
    
    @property
    def event_x_object_attribute_value(self):
        '''
        Get events x object attribute values

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with events x object attribute values
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_x_object_attribute_value
    
    @property
    def event_x_object_relation(self):
        '''
        Get events x object relations

        Parameters
        ----------
        None
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with events x object relations
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_x_object_relation
    
    @property
    def log(self):
        '''
        Get events logs

        Parameters
        ----------
        None
        
        Returns
        -------
        list
            List with events logs
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__log
    
    @property
    def current_state(self):
        '''
        Get current state

        Parameters
        ----------
        None
        
        Returns
        -------
        dict
            Dictionary with current state
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__current_state
    
    @property
    def event_counter(self):
        '''
        Get event counter

        Parameters
        ----------
        None
        
        Returns
        -------
        int
            Event counter
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        return self.__event_counter


def dump_json(file_name, OCED_model):
    '''
    Dump OCED model to JSON file
    
    Parameters
    ----------
    file_name : str
        JSON file name
    
    OCED_model : OCED
        OCED model
    
    Returns
    -------
    None
    
    Raises
    ------
    TypeError
        - If file_name is not a string
        - If OCED_model is not an OCED object
    ValueError
        - If file_name does not end with .json
    
    Notes
    -----
    None
    
    Examples
    --------
    None
    '''
    # check file_name
    if not isinstance(file_name, str):
        raise TypeError('file_name must be a string')
    if not file_name.endswith('.json'):
        raise ValueError('file_name must be a JSON file')
    # check OCED model
    if not isinstance(OCED_model, OCED):
        raise TypeError('OCED_model must be an OCED object')
    # create data
    data = {
        'event': OCED_model._OCED__event.to_dict(orient='records'),
        'event_type': OCED_model._OCED__event_type.to_dict(orient='records'),
        'event_time': OCED_model._OCED__event_time.to_dict(orient='records'),
        'event_attribute_name': OCED_model._OCED__event_attribute_name.to_dict(orient='records'),
        'event_attribute_value': OCED_model._OCED__event_attribute_value.to_dict(orient='records'),
        'object': OCED_model._OCED__object.to_dict(orient='records'),
        'object_type': OCED_model._OCED__object_type.to_dict(orient='records'),
        'object_attribute_name': OCED_model._OCED__object_attribute_name.to_dict(orient='records'),
        'object_attribute_value': OCED_model._OCED__object_attribute_value.to_dict(orient='records'),
        'object_relation': OCED_model._OCED__object_relation.to_dict(orient='records'),
        'object_relation_type': OCED_model._OCED__object_relation_type.to_dict(orient='records'),
        'event_x_object': OCED_model._OCED__event_x_object.to_dict(orient='records'),
        'event_x_object_attribute_value': OCED_model._OCED__event_x_object_attribute_value.to_dict(orient='records'),
        'event_x_object_relation': OCED_model._OCED__event_x_object_relation.to_dict(orient='records'),
        'log': OCED_model._OCED__log,
        'current_state': OCED_model._OCED__current_state,
        'event_counter': OCED_model._OCED__event_counter
    }
    # write JSON file
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)


def dump_xml(file_name, OCED_model):
    '''
    Dump OCED model to XML file
    
    Parameters
    ----------
    file_name : str
        XML file name
    OCED_model : OCED
        OCED model
    
    Returns
    -------
    None
    
    Raises
    ------
    TypeError
        - If file_name is not a string
        - If OCED_model is not an OCED object
    ValueError
        - If file_name does not end with .xml
    
    Notes
    -----
    None
    
    Examples
    --------
    None
    '''
    # check file_name
    if not isinstance(file_name, str):
        raise TypeError('file_name must be a string')
    if not file_name.endswith('.xml'):
        raise ValueError('file_name must be a XML file')
    # check OCED model
    if not isinstance(OCED_model, OCED):
        raise TypeError('OCED_model must be an OCED object')
    # create root
    root = ET.Element('OCED')
    # append event to root
    if not OCED_model._OCED__event.empty:
        event = ET.fromstring(OCED_model._OCED__event.to_xml(root_name='event'))
        root.append(event)
    # append event_type to root
    if not OCED_model._OCED__event_type.empty:
        event_type = ET.fromstring(OCED_model._OCED__event_type.to_xml(root_name='event_type'))
        root.append(event_type)
    # append event_time to root
    if not OCED_model._OCED__event_time.empty:
        event_time = ET.fromstring(OCED_model._OCED__event_time.to_xml(root_name='event_time'))
        root.append(event_time)
    # append event_attribute_name to root
    if not OCED_model._OCED__event_attribute_name.empty:
        event_attribute_name = ET.fromstring(OCED_model._OCED__event_attribute_name.to_xml(root_name='event_attribute_name'))
        root.append(event_attribute_name)
    # append event_attribute_value to root
    if not OCED_model._OCED__event_attribute_value.empty:
        event_attribute_value = ET.fromstring(OCED_model._OCED__event_attribute_value.to_xml(root_name='event_attribute_value'))
        root.append(event_attribute_value)
    # append object to root
    if not OCED_model._OCED__object.empty:
        object = ET.fromstring(OCED_model._OCED__object.to_xml(root_name='object'))
        root.append(object)
    # append object_type to root
    if not OCED_model._OCED__object_type.empty:
        object_type = ET.fromstring(OCED_model._OCED__object_type.to_xml(root_name='object_type'))
        root.append(object_type)
    # append object_attribute_name to root
    if not OCED_model._OCED__object_attribute_name.empty:
        object_attribute_name = ET.fromstring(OCED_model._OCED__object_attribute_name.to_xml(root_name='object_attribute_name'))
        root.append(object_attribute_name)
    # append object_attribute_value to root
    if not OCED_model._OCED__object_attribute_value.empty:
        object_attribute_value = ET.fromstring(OCED_model._OCED__object_attribute_value.to_xml(root_name='object_attribute_value'))
        root.append(object_attribute_value)
    # append object_relation to root
    if not OCED_model._OCED__object_relation.empty:
        object_relation = ET.fromstring(OCED_model._OCED__object_relation.to_xml(root_name='object_relation'))
        root.append(object_relation)
    # append object_relation_type to root
    if not OCED_model._OCED__object_relation_type.empty:
        object_relation_type = ET.fromstring(OCED_model._OCED__object_relation_type.to_xml(root_name='object_relation_type'))
        root.append(object_relation_type)
    # append event_x_object to root
    if not OCED_model._OCED__event_x_object.empty:
        event_x_object = ET.fromstring(OCED_model._OCED__event_x_object.to_xml(root_name='event_x_object'))
        root.append(event_x_object)
    # append event_x_object_attribute_value to root
    if not OCED_model._OCED__event_x_object_attribute_value.empty:
        event_x_object_attribute_value = ET.fromstring(OCED_model._OCED__event_x_object_attribute_value.to_xml(root_name='event_x_object_attribute_value'))
        root.append(event_x_object_attribute_value)
    # append event_x_object_relation to root
    if not OCED_model._OCED__event_x_object_relation.empty:
        event_x_object_relation = ET.fromstring(OCED_model._OCED__event_x_object_relation.to_xml(root_name='event_x_object_relation'))
        root.append(event_x_object_relation)
    # append log to root
    if OCED_model._OCED__log != {}:
        log = ET.Element('log')
        for event_id, event_log in OCED_model._OCED__log.items():
            event = ET.SubElement(log, 'event', {'event_id': str(event_id)})
            for qualifier_log in event_log:
                qualifier = ET.SubElement(event, 'qualifier', {'qualifier': qualifier_log['qualifier']})
                arguments = ET.SubElement(qualifier, 'arguments')
                for argument_name, argument_value in qualifier_log['arguments'].items():
                    ET.SubElement(arguments, 'argument', {'name': argument_name}).text = str(argument_value)
        root.append(log)
    # append current_state to root
    if OCED_model._OCED__current_state != {'object': {}, 'object_relation': {}, 'object_attribute_value': {}}:
        current_state = ET.Element('current_state')
        # append objects to current_state
        for object_id, object_state in OCED_model._OCED__current_state['object'].items():
            object = ET.SubElement(current_state, 'object', {'object_id': str(object_id)})
            ET.SubElement(object, 'type').text = object_state['type']
            ET.SubElement(object, 'existency').text = str(object_state['existency'])
            object_relation_ids = ET.SubElement(object, 'object_relation_ids')
            for object_relation_id in object_state['object_relation_ids']:
                ET.SubElement(object_relation_ids, 'object_relation_id').text = str(object_relation_id)
            object_attribute_value_ids = ET.SubElement(object, 'object_attribute_value_ids')
            for object_attribute_value_id in object_state['object_attribute_value_ids']:
                ET.SubElement(object_attribute_value_ids, 'object_attribute_value_id').text = str(object_attribute_value_id)
        # append object_relations to current_state
        for object_relation_id, object_relation_state in OCED_model._OCED__current_state['object_relation'].items():
            object_relation = ET.SubElement(current_state, 'object_relation', {'object_relation_id': str(object_relation_id)})
            ET.SubElement(object_relation, 'from_object_id').text = str(object_relation_state['from_object_id'])
            ET.SubElement(object_relation, 'to_object_id').text = str(object_relation_state['to_object_id'])
            ET.SubElement(object_relation, 'type').text = object_relation_state['type']
            ET.SubElement(object_relation, 'existency').text = str(object_relation_state['existency'])
        # append object_attribute_values to current_state
        for object_attribute_value_id, object_attribute_value_state in OCED_model._OCED__current_state['object_attribute_value'].items():
            object_attribute_value = ET.SubElement(current_state, 'object_attribute_value', {'object_attribute_value_id': str(object_attribute_value_id)})
            ET.SubElement(object_attribute_value, 'object_id').text = str(object_attribute_value_state['object_id'])
            ET.SubElement(object_attribute_value, 'name').text = object_attribute_value_state['name']
            ET.SubElement(object_attribute_value, 'value').text = object_attribute_value_state['value']
            ET.SubElement(object_attribute_value, 'existency').text = str(object_attribute_value_state['existency'])
        root.append(current_state)
    # append event_counter to root
    if OCED_model._OCED__event_counter != 0:
        event_counter = ET.Element('event_counter')
        event_counter.text = str(OCED_model._OCED__event_counter)
        root.append(event_counter)
    # write XML file
    tree = ET.ElementTree(root)
    ET.indent(tree, space='\t', level=0)
    tree.write(file_name, encoding='utf-8', xml_declaration=True)


def load_json(file_name):
    '''
    Load OCED model from JSON file
    
    Parameters
    ----------
    file_name : str
        JSON file name
    
    Returns
    -------
    OCED
        OCED model
    
    Raises
    ------
    TypeError
        - If file_name is not a string
    ValueError
        - If file_name does not end with .json

    Notes
    -----
    None

    Examples
    --------
    None
    '''
    # check file_name
    if not isinstance(file_name, str):
        raise TypeError('file_name must be a string')
    if not file_name.endswith('.json'):
        raise ValueError('file_name must be a JSON file')
    # load OCED model
    with open(file_name, 'r') as f:
        data = json.load(f)
    OCED_model = OCED()
    OCED_model._OCED__event = pd.DataFrame(data['event'])
    OCED_model._OCED__event_type = pd.DataFrame(data['event_type'])
    OCED_model._OCED__event_time = pd.DataFrame(data['event_time'])
    OCED_model._OCED__event_attribute_name = pd.DataFrame(data['event_attribute_name'])
    OCED_model._OCED__event_attribute_value = pd.DataFrame(data['event_attribute_value'])
    OCED_model._OCED__object = pd.DataFrame(data['object'])
    OCED_model._OCED__object_type = pd.DataFrame(data['object_type'])
    OCED_model._OCED__object_attribute_name = pd.DataFrame(data['object_attribute_name'])
    OCED_model._OCED__object_attribute_value = pd.DataFrame(data['object_attribute_value'])
    OCED_model._OCED__object_relation = pd.DataFrame(data['object_relation'])
    OCED_model._OCED__object_relation_type = pd.DataFrame(data['object_relation_type'])
    OCED_model._OCED__event_x_object = pd.DataFrame(data['event_x_object'])
    OCED_model._OCED__event_x_object_attribute_value = pd.DataFrame(data['event_x_object_attribute_value'])
    OCED_model._OCED__event_x_object_relation = pd.DataFrame(data['event_x_object_relation'])
    OCED_model._OCED__log = data['log']
    OCED_model._OCED__current_state = data['current_state']
    OCED_model._OCED__event_counter = data['event_counter']
    return OCED_model


def load_xml(file_name):
    '''
    Load OCED model from XML file
    
    Parameters
    ----------
    file_name : str
        XML file name
    
    Returns
    -------
    OCED
        OCED model
    
    Raises
    ------
    TypeError
        - If file_name is not a string
    ValueError
        - If file_name does not end with .xml
        - If file_name has an invalid XML structure
    
    Notes
    -----
    None
    
    Examples
    --------
    None
    '''
    def __child_to_df(child, data):
        '''
        Convert XML child to DataFrame
        
        Parameters
        ----------
        child : xml.etree.ElementTree.Element
            XML child
        data : dict
            Dictionary with data
        
        Returns
        -------
        pandas.DataFrame
            DataFrame with data
        
        Raises
        ------
        None
        
        Notes
        -----
        None
        
        Examples
        --------
        None
        '''
        # parse child
        for row in child:
            for column in row:
                data[column.tag].append(column.text)
        # convert to DataFrame
        df = pd.DataFrame(data).sort_values(by='index').drop(columns=['index']).reset_index(drop=True)
        # convert columns to correct type
        if 'object_existency' in df.columns:
            df['object_existency'] = df['object_existency'].astype(bool)
        elif 'object_relation_existency' in df.columns:
            df['object_relation_existency'] = df['object_relation_existency'].astype(bool)
        elif 'object_attribute_value_existency' in df.columns:
            df['object_attribute_value_existency'] = df['object_attribute_value_existency'].astype(bool)
        elif 'qualifier_index' in df.columns:
            df['qualifier_index'] = df['qualifier_index'].astype(int)
        elif 'event_id' in df.columns:
            df['event_id'] = df['event_id'].astype(int)
        return df
    # check file_name
    if not isinstance(file_name, str):
        raise TypeError('file_name must be a string')
    if not file_name.endswith('.xml'):
        raise ValueError('file_name must be a XML file')
    # load OCED model
    tree = ET.parse(file_name)
    root = tree.getroot()
    OCED_model = OCED()
    # parse root
    for child in root:
        if child.tag not in ['log', 'current_state', 'event_counter']:
            # parse event
            if child.tag == 'event':
                data = {
                    'index': [],
                    'event_id': [],
                    'event_type': [],
                    'event_time': []
                }
                OCED_model._OCED__event = __child_to_df(child, data)
            # parse event_type
            elif child.tag == 'event_type':
                data = {
                    'index': [],
                    'event_type': []
                }
                OCED_model._OCED__event_type = __child_to_df(child, data)
            # parse event_time
            elif child.tag == 'event_time':
                data = {
                    'index': [],
                    'event_time': []
                }
                OCED_model._OCED__event_time = __child_to_df(child, data)
            # parse event_attribute_name
            elif child.tag == 'event_attribute_name':
                data = {
                    'index': [],
                    'event_attribute_name': []
                }
                OCED_model._OCED__event_attribute_name = __child_to_df(child, data)
            # parse event_attribute_value
            elif child.tag == 'event_attribute_value':
                data = {
                    'index': [],
                    'event_id': [],
                    'event_attribute_name': [],
                    'event_attribute_value': []
                }
                OCED_model._OCED__event_attribute_value = __child_to_df(child, data)
            # parse object
            elif child.tag == 'object':
                data = {
                    'index': [],
                    'object_id': [],
                    'object_type': [],
                    'object_existency': []
                }
                OCED_model._OCED__object = __child_to_df(child, data)
            # parse object_type
            elif child.tag == 'object_type':
                data = {
                    'index': [],
                    'object_type': []
                }
                OCED_model._OCED__object_type = __child_to_df(child, data)
            # parse object_attribute_name
            elif child.tag == 'object_attribute_name':
                data = {
                    'index': [],
                    'object_attribute_name': []
                }
                OCED_model._OCED__object_attribute_name = __child_to_df(child, data)
            # parse object_attribute_value
            elif child.tag == 'object_attribute_value':
                data = {
                    'index': [],
                    'object_attribute_value_id': [],
                    'object_id': [],
                    'object_attribute_name': [],
                    'object_attribute_value': [],
                    'object_attribute_value_existency': []
                }
                OCED_model._OCED__object_attribute_value = __child_to_df(child, data)
            # parse object_relation
            elif child.tag == 'object_relation':
                data = {
                    'index': [],
                    'object_relation_id': [],
                    'from_object_id': [],
                    'to_object_id': [],
                    'object_relation_type': [],
                    'object_relation_existency': []
                }
                OCED_model._OCED__object_relation = __child_to_df(child, data)
            # parse object_relation_type
            elif child.tag == 'object_relation_type':
                data = {
                    'index': [],
                    'object_relation_type': []
                }
                OCED_model._OCED__object_relation_type = __child_to_df(child, data)
            # parse event_x_object
            elif child.tag == 'event_x_object':
                data = {
                    'index': [],
                    'event_id': [],
                    'object_id': [],
                    'qualifier_type': [],
                    'qualifier_index': []
                }
                OCED_model._OCED__event_x_object = __child_to_df(child, data)
            # parse event_x_object_attribute_value
            elif child.tag == 'event_x_object_attribute_value':
                data = {
                    'index': [],
                    'event_id': [],
                    'object_attribute_value_id': [],
                    'qualifier_type': [],
                    'qualifier_index': []
                }
                OCED_model._OCED__event_x_object_attribute_value = __child_to_df(child, data)
            # parse event_x_object_relation
            elif child.tag == 'event_x_object_relation':
                data = {
                    'index': [],
                    'event_id': [],
                    'object_relation_id': [],
                    'qualifier_type': [],
                    'qualifier_index': []
                }
                OCED_model._OCED__event_x_object_relation = __child_to_df(child, data)
            # raise exception
            else:
                raise ValueError('Unknown tag: {}'.format(child.tag))
        # parse log
        elif child.tag == 'log':
            # Iterate through events
            for event in child:
                event_id = event.get('event_id')
                qualifiers = []
                # Iterate through qualifiers
                for qualifier in event.findall('qualifier'):
                    qualifier_dict = {
                        'qualifier': qualifier.get('qualifier'),
                        'arguments': {}
                    }
                    # Iterate through arguments
                    for argument in qualifier.find('arguments'):
                        qualifier_dict['arguments'][argument.get('name')] = argument.text
                    qualifiers.append(qualifier_dict)
                OCED_model._OCED__log[event_id] = qualifiers
        # parse current_state
        elif child.tag == 'current_state':
            # Iterate through objects
            for elem in child.findall('object'):
                object_id = elem.get('object_id')
                OCED_model._OCED__current_state['object'][object_id] = {
                    "type": elem.find('type').text,
                    "existency": elem.find('existency').text.lower() == 'true',
                    "object_relation_ids": [rel.text for rel in elem.find('object_relation_ids')],
                    "object_attribute_value_ids": [val.text for val in elem.find('object_attribute_value_ids')]
                }
            # Iterate through object_attribute_values
            for elem in child.findall('object_relation'):
                object_relation_id = elem.get('object_relation_id')
                OCED_model._OCED__current_state['object_relation'][object_relation_id] = {
                    "type": elem.find('type').text,
                    "existency": elem.find('existency').text.lower() == 'true',
                    "from_object_id": elem.find('from_object_id').text,
                    "to_object_id": elem.find('to_object_id').text
                }
            # Iterate through object_attribute_values
            for elem in child.findall('object_attribute_value'):
                object_attribute_value_id = elem.get('object_attribute_value_id')
                OCED_model._OCED__current_state['object_attribute_value'][object_attribute_value_id] = {
                    "name": elem.find('name').text,
                    "value": elem.find('value').text,
                    "existency": elem.find('existency').text.lower() == 'true',
                    "object_id": elem.find('object_id').text
                }
        # parse event_counter
        elif child.tag == 'event_counter':
            OCED_model._OCED__event_counter = int(child.text)
        # raise exception
        else:
            raise ValueError('Unknown tag: {}'.format(child.tag))
    return OCED_model