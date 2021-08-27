# Models should register themselves here
# with all the names that can be used to find them
# and map it to their actual name

# from .model import ModelClass

def _extract_table_names() -> dict:
    """
    Pull out the table and plural tables names from all tables.
    """
    table_map = {}
    name_to_class_map = {}
    for _class in Base.__subclasses__():
        table_map[_class.__tablename__] = _class.__tablename__
        name_to_class_map[_class.__tablename__] = _class
        try:
            table_map[_class.plural_tablename] = _class.__tablename__
            name_to_class_map[_class.plural_tablename] = _class
        except AttributeError:
            continue
    return table_map, name_to_class_map

TABLE_NAME_MAP, NAME_TO_CLASS = _extract_table_names()