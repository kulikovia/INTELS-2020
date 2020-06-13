import csv


class src_node:

    def start(self, model_type, node_type, id, name, parent_id):
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id



class src_model:

    def start(self, file_name, model1):
        model = []
        with open(file_name) as f_obj:
            csv_dict_reader_models(f_obj, model)
        self.model1 = model

class req_model:

    def start(self, file_name, model1):
        model = []
        with open(file_name) as f_obj:
            csv_dict_reader_models(f_obj, model)
        self.model1 = model



class base_node:

    def start(self, base_id, model_type, node_type, id, name, parent_id):
        self.base_id = base_id
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.base_parent_id = base_parent_id

class base_link:
    def start(self, id, src_link, dist_link, rule, notes):
        self.id = id
        self.src_link = src_link
        self.dist_link = dist_link
        self.rule = rule
        self.notes = notes

class base_rules:
    def start(self, src_node_type, dist_node_type, rule):
        self.src_node_type = src_node_type
        self.dist_node_type = dist_node_type
        self.rule = rule

class base_requirements:
    def start(self, model_type, node_type, id, name):
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.base_id = base_id




class base_model:
    def start(self):
        self.model = []
        self.model_req = []
        self.links = []
        self.links_req = []
        self.requirements = []

    def add_model(self, src_model):
        j = len(self.model)
        for i in range(len(src_model.model1)):
            self.model.append(base_node())
            self.model[j].base_id = j
            self.model[j].model_type = src_model.model1[i].model_type
            self.model[j].node_type = src_model.model1[i].node_type
            self.model[j].id = src_model.model1[i].id
            self.model[j].name = src_model.model1[i].name
            self.model[j].parent_id = src_model.model1[i].parent_id
            self.model[j].base_parent_id = 0
            print(self.model[j].base_id, self.model[j].model_type, self.model[j].node_type, self.model[j].id, self.model[j].name, self.model[j].parent_id, self.model[j].base_parent_id)
            j = j + 1

    def id_normalisation(self):
        for i in range(len(self.model)):
            if self.model[i].base_parent_id == 0:
                for j in range(len(self.model)):
                    if (self.model[j].model_type == self.model[i].model_type) and (self.model[j].id == self.model[i].parent_id):
                        self.model[i].base_parent_id = self.model[j].base_id
            print(self.model[i].base_id, self.model[i].model_type, self.model[i].node_type, self.model[i].id, self.model[i].name, self.model[i].parent_id, self.model[i].base_parent_id)

    def create_base_links(self):
        j=0
        for i in range(len(self.model)):
            if self.model[i].base_parent_id != 0:
                k = self.model[i].base_parent_id
                if self.model[i].model_type == self.model[k].model_type:
                    self.links.append(base_link())
                    self.links[j].start(j ,self.model[i].base_parent_id, self.model[i].base_id, 'includes', 0)
                    print(self.links[j].id, self.links[j].src_link, self.links[j].dist_link, self.links[j].rule)
                    j = j+1
        with open('Links_rules.csv') as f_obj:
            self.rules = csv_dict_reader_rules(f_obj)

        for i in range(len(self.model)):
            if self.model[i].base_parent_id != 0:
                k = self.model[i].base_parent_id
                if self.model[i].node_type != self.model[k].node_type:
                    src_id = self.model[i].base_parent_id
                    dist_id = self.model[i].base_id
                    for n in range(len(self.rules)):
                        if (self.model[src_id].node_type == self.rules[n].src_node_type) and (self.model[dist_id].node_type == self.rules[n].dist_node_type):
                            self.links.append(base_link())
                            self.links[j].id = j
                            self.links[j].src_link = src_id
                            self.links[j].dist_link = dist_id
                            self.links[j].rule = self.rules[n].rule
                            print(self.links[j].id, self.links[j].src_link, self.links[j].dist_link, self.links[j].rule)
                            j = j+1

    def use_requirements(self, req_obj):
        # Rejecting nodes from the base model
        l = 0
        for i in range(len(self.model)):
            for j in range(len(req_obj.model1)):
                if (self.model[i].model_type == req_obj.model1[j].model_type) and (self.model[i].node_type == req_obj.model1[j].node_type) and (self.model[i].id == req_obj.model1[j].id) and (self.model[i].name == req_obj.model1[j].name):
                    self.model_req.append(base_node())
                    self.model_req[l].base_id = -1
                    self.model_req[l].base_parent_id = -1
                    self.model_req[l].model_type = self.model[i].model_type
                    self.model_req[l].node_type = self.model[i].node_type
                    self.model_req[l].name = self.model[i].name
                    self.model_req[l].id = self.model[i].id
                    self.model_req[l].parent_id = self.model[i].parent_id
                    print('+++', self.model_req[l].base_id, self.model_req[l].model_type, self.model_req[l].node_type, self.model_req[l].id,
                          self.model_req[l].name, self.model_req[l].parent_id, self.model_req[l].base_parent_id)
                    l = l + 1
   # Adding nodes from the base model
        l = len(self.model_req)
        for i in range(len(req_obj.model1)):
            p = 0
            for j in range(len(self.model_req)):
                if (self.model_req[j].model_type == req_obj.model1[i].model_type) and (self.model_req[j].node_type == req_obj.model1[i].node_type) and (self.model_req[j].id == req_obj.model1[i].id):
                    p = p + 1
            if p == 0:
                self.model_req.append(base_node())
                self.model_req[l].base_id = -1
                self.model_req[l].base_parent_id = -1
                self.model_req[l].model_type = req_obj.model1[i].model_type
                self.model_req[l].node_type = req_obj.model1[i].node_type
                self.model_req[l].name = req_obj.model1[i].name
                self.model_req[l].id = req_obj.model1[i].id
                self.model_req[l].parent_id = req_obj.model1[i].parent_id
                print('0+++0', self.model_req[l].base_id, self.model_req[l].model_type,
                                  self.model_req[l].node_type, self.model_req[l].id,
                                  self.model_req[l].name, self.model_req[l].parent_id, self.model_req[l].base_parent_id)
                l = l + 1
        # ID normalisation
        for i in range(len(self.model_req)):
            self.model_req[i].base_id = i
        for i in range(len(self.model_req)):
            if self.model_req[i].base_parent_id == -1:
                for j in range(len(self.model_req)):
                    if (self.model_req[j].model_type == self.model_req[i].model_type) and (self.model_req[j].id == self.model_req[i].parent_id):
                        self.model_req[i].base_parent_id = self.model_req[j].base_id
            print(self.model_req[i].base_id, self.model_req[i].model_type, self.model_req[i].node_type, self.model_req[i].id, self.model_req[i].name, self.model_req[i].parent_id, self.model_req[i].base_parent_id)

    def create_req_base_links(self):
        j=0
        for i in range(len(self.model_req)):
            if self.model_req[i].base_parent_id != -1:
                k = self.model_req[i].base_parent_id
                if self.model_req[i].model_type == self.model_req[k].model_type:
                    self.links_req.append(base_link())
                    self.links_req[j].start(j ,self.model_req[i].base_parent_id, self.model_req[i].base_id, 'includes', 0)
                    print(self.links_req[j].id, self.links_req[j].src_link, self.links_req[j].dist_link, self.links_req[j].rule)
                    j = j+1
        for i in range(len(self.model_req)):
            if self.model_req[i].base_parent_id != -1:
                k = self.model_req[i].base_parent_id
                if self.model_req[i].node_type != self.model_req[k].node_type:
                    src_id = self.model_req[i].base_parent_id
                    dist_id = self.model_req[i].base_id
                    for n in range(len(self.rules)):
                        if (self.model_req[src_id].node_type == self.rules[n].src_node_type) and (self.model_req[dist_id].node_type == self.rules[n].dist_node_type):
                            self.links_req.append(base_link())
                            self.links_req[j].id = j
                            self.links_req[j].src_link = src_id
                            self.links_req[j].dist_link = dist_id
                            self.links_req[j].rule = self.rules[n].rule
                            print(self.links_req[j].id, self.links_req[j].src_link, self.links_req[j].dist_link, self.links_req[j].rule)
                            j = j+1



def csv_dict_reader_models(file_obj, model):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    i=0
    for line in reader:
        model.append(src_node())
        model[i].model_type = line["MODEL_TYPE"]
        model[i].node_type = line["NODE_TYPE"]
        model[i].id = line["ID"]
        model[i].name = line["NAME"]
        model[i].parent_id = line["PARENT_ID"]
        print(model[i].model_type, model[i].node_type, model[i].id, model[i].name, model[i].parent_id)
        i = i+1
    return model

def csv_dict_reader_rules(file_obj_rules):
    """
    Read a CSV file using csv.DictReader
    """
    rules = []
    reader = csv.DictReader(file_obj_rules, delimiter=',')

    i=0
    for line in reader:
        rules.append(base_rules())
        rules[i].src_node_type = line["SRC_NODE_TYPE"]
        rules[i].dist_node_type = line["DIST_NODE_TYPE"]
        rules[i].rule = line["RULE"]
        print(rules[i].src_node_type, rules[i].dist_node_type, rules[i].rule)
        i = i+1
    return rules

def csv_dict_reader_requirements(file_obj_rules):
    """
    Read a CSV file using csv.DictReader
    """
    requirements = []
    reader = csv.DictReader(file_obj_rules, delimiter=',')

    i=0
    for line in reader:
        requirements.append(base_requirements())
        requirements[i].model_type = line["MODEL_TYPE"]
        requirements[i].node_type = line["NODE_TYPE"]
        requirements[i].id = line["ID"]
        requirements[i].name = line["NAME"]
        print(requirements[i].model_type, requirements[i].node_type, requirements[i].id, requirements[i].id)
        i = i+1
    return requirements

def create_rdf_model(model, links, file_name):
    # Open SPARQL file
    spql = open(file_name, "wt")
    # Add header
    header = str(
        "<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\n>")

    spql.write(header)

    #Create nodes
    for i in range(len(model)):
        body = str("\n<rdf:Description rdf:about='http://127.0.0.1/") + str(model[i].name) + str("/'>\n<my:has_id>") + str(model[i].base_id) + str("</my:has_id>\n<my:has_type>") + str(model[i].node_type) + str("</my:has_type>\n<my:has_description>") + str("Model type: ") + str(model[i].model_type) + str(", Node type: ") + str(model[i].node_type) + str(", Node name: ") + str(model[i].name)+ str("</my:has_description>\n</rdf:Description>\n")
        spql.write(body)

    #Create links
    for i in range(len(links)):
        body = str("\n<rdf:Description rdf:about='http://127.0.0.1/") + str(model[links[i].src_link].name) + str("/'>\n<my:") + str(links[i].rule) +str(">") + str("\n<rdf:Description rdf:about='http://127.0.0.1/") + str(model[links[i].dist_link].name) + str("/'>\n</rdf:Description>\n</my:") + str(links[i].rule) +str(">\n</rdf:Description>\n")
        spql.write(body)

    #Create footer
    spql.write("\n</rdf:RDF>\n")
    spql.close()
    return 1


if __name__ == "__main__":
    #Import VOD src model
    vod_obj = src_model()
    vod_obj.start("VOD_1.csv", model1 = [])
    print(vod_obj.model1[1].model_type)
    # Import Billing src model
    billing_obj = src_model()
    billing_obj.start("Billing_1.csv", model1=[])
    print(billing_obj.model1[1].model_type)
    # Import Entitlements src model
    entitlements_obj = src_model()
    entitlements_obj.start("Entitlements_1.csv", model1=[])
    print(entitlements_obj.model1[1].model_type)
    # Create base model
    base_obj = base_model()
    base_obj.start()
    # Add VOD model
    base_obj.add_model(vod_obj)
    # Add billing model
    base_obj.add_model(billing_obj)
    # Add entitlement model
    base_obj.add_model(entitlements_obj)
    # ID normalisation
    base_obj.id_normalisation()
    # Base links creation
    base_obj.create_base_links()
    # Create requirements object
    req_obj = req_model()
    req_obj.start("Requirements_1.csv", model1=[])
    # Using requirements
    base_obj.use_requirements(req_obj)
    # Create links for model_req
    base_obj.create_req_base_links()
    # Create base RDF model
    create_rdf_model(base_obj.model, base_obj.links, 'Base_rdf_1.nq')
    # Create user req. RDF model
    create_rdf_model(base_obj.model_req, base_obj.links_req, 'Req_rdf_1.nq')