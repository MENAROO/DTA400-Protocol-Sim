import simpy
import random
import matplotlib.pyplot as plt

# Constants
SIM_DURATION = 1000  # simulation time
PACKET_GEN_RATE = 5  # packets generated per time unit
MAX_LATENCY_OSPF = 5
MAX_LATENCY_EIGRP = 3
MAX_LATENCY_BGP = 8

# Variables to store results
latency_results = {'OSPF': [], 'EIGRP': [], 'BGP': []}
packet_loss_results = {'OSPF': 0, 'EIGRP': 0, 'BGP': 0}  # Initialize packet_loss as integers


def packet_transmission(env, protocol, results):
    while True:
        yield env.timeout(random.expovariate(PACKET_GEN_RATE))
        transmission_time = random.uniform(1, MAX_LATENCY_OSPF if protocol == 'OSPF'
        else MAX_LATENCY_EIGRP if protocol == 'EIGRP'
        else MAX_LATENCY_BGP)

        if transmission_time > (MAX_LATENCY_BGP - 2 if protocol == 'BGP' else
        MAX_LATENCY_EIGRP - 1 if protocol == 'EIGRP' else
        MAX_LATENCY_OSPF - 1):
            results['packet_loss'][protocol] += 1  # Access packet_loss_results dictionary correctly
        else:
            results['latency'][protocol].append(transmission_time)


def run_simulation(protocol):
    env = simpy.Environment()
    results = {'latency': latency_results, 'packet_loss': packet_loss_results}
    env.process(packet_transmission(env, protocol, results))
    env.run(until=SIM_DURATION)


# Run simulations
for protocol in latency_results.keys():
    run_simulation(protocol)

# Calculate average latency
average_latency = {protocol: sum(latency) / len(latency) if len(latency) > 0 else 0
                   for protocol, latency in latency_results.items()}

# Calculate packet loss rate
packet_loss_rate = {protocol: packet_loss / (SIM_DURATION * PACKET_GEN_RATE)
                    for protocol, packet_loss in packet_loss_results.items()}

# Plot results
plt.figure(figsize=(14, 6))

# Plot Average Latency by Protocol
plt.subplot(1, 2, 1)
plt.bar(average_latency.keys(), average_latency.values(), color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.xlabel('Protocol', fontsize=12)
plt.ylabel('Average Latency (ms)', fontsize=12)
plt.title('Average Latency by Protocol', fontsize=14)
plt.ylim(0, max(average_latency.values()) + 1)  # Adjust y-axis limit for better spacing
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add horizontal grid lines for readability
for index, value in enumerate(average_latency.values()):
    plt.text(index, value + 0.1, f'{value:.2f}', ha='center', fontsize=10)  # Show values on top of bars

# Plot Packet Loss Rate by Protocol
plt.subplot(1, 2, 2)
plt.bar(packet_loss_rate.keys(), packet_loss_rate.values(), color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.xlabel('Protocol', fontsize=12)
plt.ylabel('Packet Loss Rate (%)', fontsize=12)
plt.title('Packet Loss Rate by Protocol', fontsize=14)
plt.ylim(0, max(packet_loss_rate.values()) + 0.02)  # Adjust y-axis limit for better spacing
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add horizontal grid lines for readability
for index, value in enumerate(packet_loss_rate.values()):
    plt.text(index, value + 0.001, f'{value:.4f}', ha='center', fontsize=10)  # Show values on top of bars

plt.tight_layout(pad=3.0)  # Adjust padding for better layout
plt.show()
