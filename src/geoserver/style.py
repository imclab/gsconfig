from geoserver.support import ResourceInfo, url, xml_property
import geoserver.workspace as ws

class Style(ResourceInfo):
    def __init__(self, catalog, name):
        super(Style, self).__init__()
        assert isinstance(name, basestring)

        self.catalog = catalog
        self.name = name
        self._sld_dom = None

    @property
    def href(self):
        return url(self.catalog.service_url, ["styles", self.name + ".xml"])

    def body_href(self):
        return url(self.catalog.service_url, ["styles", self.name + ".sld"])

    filename = xml_property("filename")

    def _get_sld_dom(self):
        if self._sld_dom is None:
            self._sld_dom = self.catalog.get_xml(self.body_href())
        return self._sld_dom

    @property
    def sld_title(self):
        user_style = self._get_sld_dom().find("{http://www.opengis.net/sld}NamedLayer/{http://www.opengis.net/sld}UserStyle")
        title_node = user_style.find("{http://www.opengis.net/sld}Title")
        return title_node.text if title_node is not None else None

    @property
    def sld_name(self):
        user_style = self._get_sld_dom().find("{http://www.opengis.net/sld}NamedLayer/{http://www.opengis.net/sld}UserStyle")
        name_node = user_style.find("{http://www.opengis.net/sld}Name")
        return name_node.text if name_node is not None else None

    @property
    def sld_body(self):
        content = self.catalog.http.request(self.body_href())[1]
        return content

    def update_body(self, body):
        headers = { "Content-Type": "application/vnd.ogc.sld+xml" }
        self.catalog.http.request(
            self.body_href(), "PUT", body, headers)



class Workspace_Style(Style):
    def __init__(self, catalog, workspace, name):
        super(Workspace_Style, self).__init__(catalog, name)
        
        assert isinstance(workspace, ws.Workspace)
        self.workspace = workspace


    @property
    def href(self):
        return url(self.catalog.service_url, ["workspaces", self.workspace.name, "styles", self.name + ".xml"])

    def body_href(self):
        return url(self.catalog.service_url, ["workspaces", self.workspace.name, "styles", self.name + ".sld"])