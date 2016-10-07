########################################################################
#  Created 2016 based on code Copyright (C) 2013 Sol Birnbaum
# 
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
########################################################################

from ..utils.wapxml import wapxmltree, wapxmlnode


class Search:
    """https://msdn.microsoft.com/en-us/library/gg675482(v=exchg.80).aspx

    Currently for DocumentLibrary searches only.
    """

    @staticmethod
    def build(unc_path, return_range='0-999', username=None, password=None):

        xmldoc_req = wapxmltree()
        xmlrootnode = wapxmlnode("Search")
        xmldoc_req.set_root(xmlrootnode, "search")

        store_node = wapxmlnode("Store", xmlrootnode)

        # "GAL" to search the Global Address List.
        # "Mailbox" to search the mailbox.
        # "DocumentLibrary" to search a Windows SharePoint Services library or a UNC library.
        name_node = wapxmlnode("Name", store_node, "DocumentLibrary")

        query_node = wapxmlnode("Query", store_node)
        equal_to_node = wapxmlnode("EqualTo", query_node)
        link_id = wapxmlnode("documentlibrary:LinkId", equal_to_node)
        value_node = wapxmlnode("Value", equal_to_node, unc_path)

        options_node = wapxmlnode("Options", store_node)
        range_node = wapxmlnode("Range", options_node, return_range)

        if username is not None:
            username_node = wapxmlnode("UserName", options_node, username)
        if password is not None:
            password_node = wapxmlnode("Password", options_node, password)

        return xmldoc_req

    @staticmethod
    def parse(wapxml):

        namespace = "search"
        root_tag = "Search"

        root_element = wapxml.get_root()
        if root_element.get_xmlns() != namespace:
            raise AttributeError("Xmlns '%s' submitted to '%s' parser. Should be '%s'." % (root_element.get_xmlns(), root_tag, namespace))
        if root_element.tag != root_tag:
            raise AttributeError("Root tag '%s' submitted to '%s' parser. Should be '%s'." % (root_element.tag, root_tag, root_tag))

        children = root_element.get_children()

        status = None
        results = []

        for element in children:
            if element.tag is "Status":
                status = element.text
                if status != "1":
                    print "%s Exception: %s" % (root_tag, status)
            elif element.tag == "Response":

                properties = element.basic_xpath('Store/Result/Properties')
                for properties_el in properties:
                    result = {}
                    properties_children = properties_el.get_children()
                    for prop_el in properties_children:
                        prop = prop_el.tag.partition(':')[2]
                        result[prop] = prop_el.text
                    results.append(result)

        return status, results

