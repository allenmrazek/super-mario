from abc import ABC, abstractmethod
from .entity import Entity, Layer
from .characters import LevelEntity
from pygame.sprite import Rect
from enum import IntFlag
from util import copy_vector
from util import make_vector


class EntityManager:
    ENTITY_UPDATE_RANGE_MULTIPLIER = 1.25

    def __init__(self, update_layer_ordering: list, draw_layer_ordering):
        assert update_layer_ordering is not None
        assert draw_layer_ordering is not None

        self.update_ordering = update_layer_ordering
        self.draw_ordering = draw_layer_ordering

        self.layers = dict(zip([layer_name for layer_name in Layer], [list() for _ in Layer]))

    @staticmethod
    def create_default():
        # create a default entity manager. This is standard gameplay
        update_order = [Layer.Background, Layer.Block, Layer.Spawner, Layer.Trigger,
                    Layer.Enemy, Layer.Mario, Layer.Active, Layer.Interface, Layer.Overlay]

        draw_order = [Layer.Background, Layer.Block,
                    Layer.Enemy, Layer.Mario, Layer.Active, Layer.Interface, Layer.Overlay]

        return EntityManager(update_order, draw_order)

    @staticmethod
    def create_editor():
        # create entity manager for editor. This has its own manager because the editor has layers that
        # won't typically be drawn during play, but are relevant while editing (spawners, triggers)
        ordering = [Layer.Background, Layer.Block, Layer.Spawner, Layer.Trigger,
                    Layer.Enemy, Layer.Mario, Layer.Active, Layer.Interface, Layer.Overlay]

        return EntityManager(ordering, ordering)

    def register(self, *args):
        try:
            iterator = iter(*args)

            for item in iterator:
                self._register_internal(item)

        except TypeError:
            for item in args:
                if isinstance(item, Entity):
                    self._register_internal(*args)
                else:
                    self.register(item)

    def _register_internal(self, entity):
        assert entity.layer in self.layers.keys()
        self.layers[entity.layer].append(entity)

    def unregister(self, entity):
        assert isinstance(entity, Entity)
        assert entity.layer in self.layers.keys()
        assert entity in self.layers[entity.layer]

        self.layers[entity.layer].remove(entity)

    def draw(self, screen, view_rect):
        # draw only screen and a quarter
        offscreen_range = view_rect.width * (EntityManager.ENTITY_UPDATE_RANGE_MULTIPLIER - 1)

        minx = view_rect.left - offscreen_range
        maxx = view_rect.right + offscreen_range

        for layer in self.draw_ordering:
            self.draw_layer(layer, screen, view_rect, minx, maxx)

    def draw_layer(self, layer, screen, view_rect, minx=None, maxx=None):
        assert layer in self.layers

        for entity in self.layers[layer]:
            xpos = entity.position.x

            if not minx or xpos >= minx:
                if not maxx or xpos <= maxx:
                    if hasattr(entity, "enabled"):
                        if entity.enabled:
                            entity.draw(screen, view_rect)
                    else:
                        entity.draw(screen, view_rect)

    def update(self, dt, view_rect):
        # update only screen and a quarter
        offscreen_range = view_rect.width * (EntityManager.ENTITY_UPDATE_RANGE_MULTIPLIER - 1)

        minx = view_rect.left - offscreen_range
        maxx = view_rect.right + offscreen_range

        for layer in self.update_ordering:
            self.update_layer(layer, dt, view_rect, minx, maxx)

    def update_layer(self, layer, dt, view_rect, minx=None, maxx=None):
        assert layer in self.layers

        entities = list(self.layers[layer])  # since entities might be removed

        for entity in entities:
            xpos = entity.position.x

            if not minx or xpos >= minx:
                if not maxx or xpos <= maxx:
                    if hasattr(entity, "enabled"):
                        if entity.enabled:
                            entity.update(dt, view_rect)
                    else:
                        entity.update(dt, view_rect)

    def serialize(self):
        values = {"__class__": self.__class__.__name__}

        for layer in self.layers:
            values[layer.name] = self._serialize_layer(layer)

        return values

    def _serialize_layer(self, layer):
        entity_values = []

        for entity in self.layers[layer]:
            if hasattr(entity, "serialize"):
                entity_values.append(entity.serialize())

        return entity_values

    def deserialize(self, level, values):
        assert values["__class__"] == self.__class__.__name__

        # clear any existing values and load new ones from disk
        for layer in self.layers:
            entity_list = self.layers[layer]

            for existing_entity in entity_list:
                if hasattr(existing_entity, "destroy"):
                    existing_entity.destroy()

            entity_list.clear()

            # find entries for this layer
            if layer.name not in values.keys():
                continue

            for entity_values in values[layer.name]:
                # create these entities
                entity = LevelEntity.build(level, entity_values)

                if entity is not None:
                    self.register(entity)

    def search_by_type(self, cls):
        found = []

        for layer in self.layers:
            for entity in self.layers[layer]:
                if isinstance(entity, cls):
                    found.append(entity)

        return found

    def get_entities_inside_region(self, rect: Rect):
        # return any entity, regardless of layer, that is intersecting with the given rect
        found = set()

        for layer in self.layers:
            for entity in self.layers[layer]:
                if rect.collidepoint(*entity.position) or rect.colliderect(entity.rect):
                    found.add(entity)

        return list(found)
