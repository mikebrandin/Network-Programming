# Mike Brandin 9/11/2021 CPSC 3600 Section 91005
# Assignment - Introduction to Python

# TODO: Import the config variable from the network_config module
from network_config import config

class RoundTripLatencyCalculator:

    def __init__(self, config):
        # TODO: Perform any required initialization. Config should be a dictionary that contains
        #       all of the parameters necessary to calculate the latency for a given path through a network
        #       The config variable should be defined in a separate file named 'network_config.py'
        self.config = config

    def calculate_total_RTT(self):
        # TODO: Compute the total round trip latency. You should use the below helper functions to break 
        #       the computation into its multiple component parts.
        #       Return the total round trip latency after computing it
        total_delay = 0
        for m in range(self.config["num_links"]):
            total_delay += self.calculate_link_contribution(m)   

        return total_delay * 2

    def calculate_link_contribution(self, hop_number):
        # TODO: Compute the total latency associated with a crossing a specific hop one-way. 
        #       You should use the below helper functions to break the computation into its multiple component parts.
        #       Return the total round trip latency after computing it
        tran_sum = self.calculate_transmission_delay(hop_number)
        proc_sum = self.calculate_processing_delay(hop_number)
        prop_sum = self.calculate_propagation_delay(hop_number)
        queu_sum = self.calculate_queuing_delay(hop_number)
        return tran_sum + proc_sum + prop_sum + queu_sum

    def calculate_transmission_delay(self, hop_number):
        # TODO: Compute the transmission delay associated with a given hop
        tran_hops = self.config["transmission_speeds"]
        
        return (self.config["packet_length"] / tran_hops[hop_number]) 

    def calculate_propagation_delay(self, hop_number):
        # TODO: Compute the propagation delay associated with a given hop
        dist_hops = self.config["distances"]
        band_hops = self.config["bandwidths"]

        return (dist_hops[hop_number] / band_hops[hop_number])

    def calculate_processing_delay(self, hop_number):
        # TODO: Compute the processing delay associated with a given hop
        proc_hops = self.config["processing_delays"]
        return proc_hops[hop_number]

    def calculate_queuing_delay(self, hop_number):
        # TODO: Compute the queuing delay associated with a given hop using the equations 
        #       delay = (0.1) / (1-delay_factor) - .1
        #       delay_factor = packet_length * average_packet_arrival_rate / bandwidth
        #       IMPORTANT: In real life, you can't predict exactly what the queueing delay will be. 
        #                  These equations roughly model what the size of the delay could be like in proportion
        #                  to how many packets are trying to move through a router at a given time
        avgpack_hops = self.config["average_packet_arrival_rates"]
        band_hops = self.config["bandwidths"]
        return ((0.1) / (1 - ((self.config["packet_length"] * avgpack_hops[hop_number]) / band_hops[hop_number]))) - .1

# You do not need to change anything in the main method. It will not be called by the testing suite, so anything
# you implement here will not register when you submit your code. It is intended for your own personal testing only
if __name__ == "__main__":
    config["packet_length"] = 8
    config["num_links"] = 2

    config["transmission_speeds"] = [1,2,3,4]
    config["processing_delays"] = [1,2,3,4]
    config["distances"] = [1,2,3,4]
    config["bandwidths"] = [1,2,3,4]
    config["average_packet_arrival_rates"] = [1,2,3,4]

    calc = RoundTripLatencyCalculator(config)

    latency = calc.calculate_total_RTT()
    print(latency)