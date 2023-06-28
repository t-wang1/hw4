import math
import json 

with open('/Users/tiffanywang/Documents/CSE 216/hw4/airport_data.json') as f:
    data = json.load(f)

with open('/Users/tiffanywang/Documents/CSE 216/hw4/edge_data.json') as f:
    edges_data = json.load(f) 

class p_tps:
    transactions = []
    num_transactions = 0
    most_recent_transaction = -1
    performing_do = False
    performing_undo = False

    def __init__(self, transactions, num_transactions, most_recent_transaction, performing_do, performing_undo):
        self.transactions = transactions
        self.num_transactions = num_transactions
        self.most_recent_transaction = most_recent_transaction
        self.performing_do = performing_do
        self.performing_undo = performing_undo
    
    def is_performing_do(self):
        return self.performing_do
    
    def is_performing_undo(self):
        return self.performing_undo

    def has_transaction_to_redo(self):
        if (self.most_recent_transaction + 1) < self.num_transactions:
            return True
        else:
            return False
    
    def has_transaction_to_undo(self):
        if (self.most_recent_transaction >= 0):
            return True
        else:
            return False
        
    def add_transaction(self, transaction):
        if (self.most_recent_transaction < 0) or (self.most_recent_transaction < len(self.transactions)-1):
            for i in range(len(self.transactions) - 1, self.most_recent_transaction, -1):
                del self.transactions[i]
            self.num_transactions = self.most_recent_transaction + 2
        else:
            self.num_transactions += 1
        
        self.transactions[self.most_recent_transaction+1] = transaction
        self.do_transaction()

    def do_transaction(self):
        if (self.has_transaction_to_redo()):
            self.performing_do = True
            transaction = self.transactions[self.most_recent_transaction+1]
            transaction.do_transaction()
            self.most_recent_transaction +=1 
            self.performing_do = False
    
    def undo_transaction(self):
        if (self.has_transaction_to_undo()):
            self.performing_undo = True
            transaction = self.transactions[self.most_recent_transaction]
            transaction.undo_transaction()
            self.most_recent_transaction -= 1
            self.performing_undo = False

    def clear_all_transactions(self):
        self.transactions = []
        self.most_recent_transaction = -1
        self.num_transactions = 0
    
    def get_size(self):
        return len(self.transactions)
    
    def get_redo_size(self):
        return self.get_size() - self.most_recent_transaction - 1
    
    def get_undo_size(self):
        return self.most_recent_transaction + 1
    
    def __str__(self):
        text = ""
        text += "--Number of Transactions: " + str(self.num_transactions) + "\n"
        text += "--Current Index on Stack: " + str(self.most_recent_transaction) + "\n"
        text += "--Current Transaction Stack: \n"
        for i in range(self.most_recent_transaction+1):
            pT = self.transactions[i]
            text += "----" + str(pT) + "\n"
        return text 

class airport:
    def __init__(self, code, latitude_degrees, latitude_minutes, longitude_degrees, longitude_minutes):
        self.code = code
        self.latitude_degrees = latitude_degrees
        self.latitude_minutes = latitude_minutes
        self.longitude_degrees = longitude_degrees
        self.longitude_minutes = longitude_minutes
    
    def get_code(self):
        return self.code

    def get_latitude_degrees(self):
        return self.latitude_degrees
    
    def get_latitude_minutes(self):
        return self.latitude_minutes

    def get_longitude_degrees(self):
        return self.longitude_degrees

    def get_longitude_minutes(self):
        return self.longitude_minutes
    
    def calculate_distance(self, a1, a2):
        PI = math.pi
        RADIAN_FACTOR = 180.0/PI
        EARTH_RADIUS = 3963.0

        lat1 = a1.latitude_degrees + a1.latitude_minutes/60.0
        lat1 = lat1 / RADIAN_FACTOR
        long1 = -a1.longitude_degrees + a1.longitude_degrees/60.0
        long1 = long1/ RADIAN_FACTOR
        lat2 = a2.latitude_degrees + a2.latitude_minutes/60.0
        lat2 = lat2 / RADIAN_FACTOR
        long2 = -a2.latitude_degrees + a2.longitude_minutes/60.0
        long2 = long2 / RADIAN_FACTOR

        x = (math.sin(lat1) * math.sin(lat2)) + (math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1))
        x2 = (math.sqrt(1.0 - (x * x)) / x)
        distance = (EARTH_RADIUS * math.atan(x2))
        return distance
    
class weighted_edge:
    def __init__(self, init_node1, init_node2, init_weight):
        self.node1 = init_node1
        self.node2 = init_node2
        self.weight = init_weight

    def get_node1(self):
        return self.node1
    
    def get_node2(self):
        return self.node2
    
    def get_weight(self):
        return self.weight

class weighted_graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
    
    def get_keys(self, keys):
        test_keys = list(self.nodes.keys())
        for key in test_keys:
            keys.append(key)

    def node_exists(self, test_node):
        if test_node in self.nodes:
            return True
        else:
            return False
        # return self.nodes.has_key(test_node)
    
    def get_edge_id(self, node1, node2):
        return str(node1) + "-" + str(node2)
    
    def add_node(self, node_id, node_data):
        self.nodes[node_id] = node_data
    
    def get_node_data(self, node_id):
        return self.nodes[node_id]
    
    def add_edge(self, node1, node2, weight):
        edge_id = self.get_edge_id(node1, node2)
        self.edges[edge_id] = weighted_edge(node1, node2, weight)
    
    def remove_edge(self, node1, node2):
        edge_id = self.get_edge_id(node1, node2)
        edge = self.edges[edge_id]

    def get_neighbors(self, neighbors, node):
        test_keys = list(self.edges.keys())
        for key in test_keys:
            index = key.index("-")
            start_node = key[0:index]
            if start_node == node:
                neighbor = key[index + 1]
                neighbors.append(neighbor)
    
    def are_neighbors(self, node1, node2):
        neighbors = []
        self.get_neighbors(neighbors, node1)
        return node2 in neighbors
    
    def get_neighbor_weight(self, node1, node2):
        if (self.are_neighbors(node1, node2)):
            edge_id = self.get_edge_id(node1, node2)
            return self.edges[edge_id].get_weight()
        
    def find_path(self, path, node1, node2):
        print("Find path from " + node1 + " to " + node2)

        if (not self.node_exists(node1) or not self.node_exists(node2)):
            return
        
        path.append(node1)

        visited = {}
        visited[node1] = node1

        while len(path) > 0:
            last = path[len(path)-1]

            neighbors = []
            self.get_neighbors(neighbors, last)

            closest_index = -1
            closest_distance = 100000.0

            for i in range(len(neighbors)):
                test_neighbor = neighbors[i]

                if test_neighbor == node2:
                    path.append(test_neighbor)
                    return
                
                if test_neighbor not in visited:
                    id = self.get_edge_id(last, test_neighbor)
                    edge = self.edges[id]
                    if edge.get_weight() < closest_distance:
                        closest_index = i 
                        closest_distance = edge.get_weight()

            if closest_index >= 0:
                closest_node = neighbors[closest_index]
                visited[closest_node] = closest_node
                path.append(closest_node)
            elif len(path) > 0:
                path.pop()

class trip_planner:
    trip_stops = []

    def __init__(self, init_trip_stops, init_code):
        self.code = init_code
        self.trip_stops = init_trip_stops
    
    def do_transaction(self):
        self.trip_stops.append(self.code)

    def undo_transaction(self):
        self.trip_stops.pop()

    def __str__():
        return "Appending Stop"
    

stops = []
graph = weighted_graph()
tps = p_tps([], 0, -1, False, False)
p_tps_description = str(tps)
print(p_tps_description)

def display_airports():
    print("Airports you can travel to and from: ")
    code = []
    graph.get_keys(code)
    for i in range(len(code)):
        if i % 10 == 0:
            print("\t")
        print(code[i])
        if i < len(code)-1:
            print(", ")
        if i % 10 == 9:
            print()
    print("\n\n")

def display_current_trip():
    print("Current Trip Stops: ")
    for i in range(len(stops)):
        print(f"\t{i + 1}. {stops[i]}")
    
    print("Current Trip Length: ")
    leg_num = 1
    trip_distance = 0.0
    leg_distance = 0.0
    output = ""
    for i in range(len(stops)):
        if leg_num < len(stops):
            output += f"\t{i + 1}. "
            last_stop = stops[leg_num-1]
            next_stop = stops[leg_num]
            route = []
            graph.find_path(route, last_stop, next_stop)
            if len(route) < 2:
                print("No route found from" + last_stop + " to " + next_stop)
            else:
                for j in range(len(route)-1):
                    a1 = graph.get_node_data(route[j])
                    a2 = graph.get_node_data(route[j+1])
                    distance = airport.calculate_distance(a1, a2)
                    leg_distance += distance
                    if j == 0:
                        print(a1.get_code())
                        print("-" + a2.get_code())
                print("Leg Distance: " + leg_distance + "miles")
            leg_num += 1
            trip_distance += leg_distance
    output += "Total Trip Distance: " + str(trip_distance) + "miles"

def display_menu():
    print("Enter a selection: ")
    print("S) Add a Stop to your Trip")
    print("U) Undo")
    print("R) Redo")
    print("E) Empty Trip")
    print("Q) Quit")
    print("-")

def process_user_input(self):
    input = print("Enter your selection: ")
    if input == "S":
        print("Enter the airport code: ")
        if graph.node_exists(input):
            neighbors = []
            graph.get_neighbors(neighbors, input)
            if len(stops) > 0:
                last_stop = stops[len(stops)-1]
                if last_stop == input:
                    print("duplicate stop error - no stop added")
                else:
                    t = trip_planner(stops, input)
                    tps.add_transaction(t)
            else:
                t = trip_planner(stops, input)
                tps.add_transaction(t)
        else:
            print("invalid airport code error - no stop added")
    elif input == "U":
        tps.undo_transaction
    elif input == "R":
        tps.do_transaction
    elif input == "E":
        tps.clear_all_transactions
    elif input == "Q":
        return False

def init_all_airports():
    for airport_data in data:
        airport_code = airport_data['airport code']
        latitude_degrees = airport_data['latitude degrees']
        latitude_minutes = airport_data['latitude minutes']
        longitude_degrees = airport_data['longitude degrees']
        longitude_minutes = airport_data['longitude minutes']
        new_airport = airport(airport_code, latitude_degrees, latitude_minutes, longitude_degrees, longitude_minutes)
        graph.add_node(airport_code, new_airport)

def init_edge(node1, node2):
    a1 = graph.get_node_data(node1)
    a2 = graph.get_node_data(node2)
    distance = a1.calculate_distance(a1, a2) 
    graph.add_edge(a1, a2, distance)
    graph.add_edge(a2, a1, distance)

def init_all_edges():
    for edge_data in edges_data:
        edge1 = edge_data['edge1']
        edge2 = edge_data['edge2']
        init_edge(edge1, edge2)

init_all_airports()
init_all_edges()
display_airports()
display_current_trip()
display_menu()
process_user_input() 

def main():
    check = True
    while(check):
        display_airports()
        display_current_trip()
        display_menu()
        check = process_user_input()

# airport_graph = weighted_graph()