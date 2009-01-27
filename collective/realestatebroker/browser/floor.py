from Products.ATContentTypes.interface.image import IATImage
from base import RealEstateBaseView
from collective.realestatebroker.adapters.interfaces import IFloorInfo
from plone.memoize.view import memoize

import logging
logger = logging.getLogger('floorview')


class FloorplansView(RealEstateBaseView):
    """docstring for FloorplansView"""

    @memoize
    def floorplans(self):
        """Return dict for displaying floors

        Return a dict like this:

        {'floors': [{'name': 'BG', 'selected': False, 'url': 'aaa'},
                    {'name': '1e', 'selected': True, 'url': 'bbb'}],
         'floorplans': ['&lt;img src=&quot;favicon.ico /&gt;']}

        Make sure to filter out floors that don't have any floorplan.

        """
        result = {}
        names = list(self.properties.getProperty('floor_names'))
        if not names:
            return
        floors = []
        selected = self.request.form.get('selected', None)
        if not selected:
            selected = names[0]
        base_url = self.context.absolute_url() + '/plans?selected='
        # Grab floorplans.
        brains = self.catalog(object_provides=IATImage.__identifier__,
                              is_floorplan=True,
                              sort_on='getObjPositionInParent',
                              path='/'.join(self.context.getPhysicalPath()))
        used_floors = []
        floorplans = []
        album = self.context.restrictedTraverse('@@realestate_album')
        for brain in brains:
            obj = brain.getObject()
            floor = IFloorInfo(obj).floor
            used_floors.append(floor)
            if floor == selected:
                floorplans.append(album.image_brain_tag(brain, scale="large"))
        result['floorplans'] = floorplans
        for name in names:
            floor = {}
            if not name in used_floors:
                continue
            floor['name'] = name
            floor['selected'] = (name == selected)
            floor['url'] = base_url + name
            floors.append(floor)
        result['floors'] = floors
        return result

    @memoize
    def floorplans_for_pdf(self):
        """Return dict for displaying floors

        Return a list like this:

        [{'floorname': '1st floor', 'photos': ['obj1', 'obj2']}]

        Make sure to filter out floors that don't have any floorplan.

        """
        floors = {}
        names = list(self.properties.getProperty('floor_names'))
        if not names:
            return
        for name in names:
            floors[name] = []
        # Grab floorplans.
        brains = self.catalog(object_provides=IATImage.__identifier__,
                         is_floorplan=True,
                         sort_on='getObjPositionInParent',
                         path='/'.join(self.context.getPhysicalPath()))
        used_floors = []
        for brain in brains:
            obj = brain.getObject()
            floor = IFloorInfo(obj).floor
            used_floors.append(floor)
            if floor in floors:
                floors[floor].append(obj)
            else:
                # Keyerror when a floorplan isn't attached to a floor...
                floor = names[0]
                IFloorInfo(obj).floor = floor
                logger.warning("Floorplan wasn't assigned to a floor. "
                               "It has now been set to %s.", floor)
                floors[floor].append(obj)
        # Filter out unused floors
        unused = [name for name in names
                  if name not in used_floors]
        for name in unused:
            del floors[name]
        # Now pack 'em up in a list: in the right order.
        result = []
        for name in names:
            if name in floors:
                result.append({'floorname': name,
                               'photos': floors[name]})
        return result
