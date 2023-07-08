
from datetime import datetime
import statistics

log_file = "sample.log"

"""
slow_server_finder reads a .log file and determines what are the slowest separating worker and frotend servers .
@params (sample) - a .log file to be loaded.
@return slow_worker_server{}, slow_frontend_server{} - Two lists with the slowest servers.
"""

def slow_server_finder(sample):

    file_log = open(log_file, 'r')

    frontend_response_times = {}

    worker_response_times = {}

    guids = {}
    # Iterates through each line of file_log
    for line in file_log:
        line_split = line.split()
        datestamp = datetime.strptime(line_split[0], '%Y-%m-%dT%H:%M:%S.%f')
        datestamp = datestamp.timestamp()

        log_date_time = datestamp
        request_GUID = line_split[1]
        action_type = line_split[2]
        server_worker_id = line_split[7]
        # Creates a list with the information of each file
        request_information = [server_worker_id, log_date_time, action_type]
        # Populates guids dictionary. The keys are the requests GUID
        # The values are a list of each step of the transaction (GET/POST, HANDLE, RESPOND)
        if request_GUID in guids:
            guids[request_GUID].append(request_information)
        else:
            guids[request_GUID] = [request_information]
    # Iterates through each key(request GUID) and populates worker_response_times and frontend_response_times dictionaries
    for guid in guids:
        # The response time of the worker server is the datestamp of the HANDLE request minus the datestamp of the GET/POST request
        if guids[guid][1][0] in worker_response_times:
            worker_response_times[guids[guid][1][0]].append(guids[guid][1][1] - guids[guid][0][1])
        else:
            worker_response_times[guids[guid][1][0]] = [guids[guid][1][1] - guids[guid][0][1]]
        # The response time of the frontend server is the datestamp of the RESPOND request minus the datestamp of the HANDLE request
        if guids[guid][2][0] in frontend_response_times:
            frontend_response_times[guids[guid][2][0]].append(guids[guid][2][1] - guids[guid][1][1])
        else:
            frontend_response_times[guids[guid][2][0]] = [guids[guid][2][1] - guids[guid][1][1]]

    worker_average_response_time = {}
    frontend_average_response_time = {}
    # Calculates the average response time for each dictionary
    for server in worker_response_times:
        worker_average_response_time[server] = sum(worker_response_times[server])/len(worker_response_times[server])

    for server in frontend_response_times:
        frontend_average_response_time[server] = sum(frontend_response_times[server])/len(frontend_response_times[server])

    worker_average_respond_list = list(worker_average_response_time.values())

    frontend_average_responde_list = list(frontend_average_response_time.values())
    # Calculates percentiles for each list of the response times
    worker_server_percentile = [round(q, 3) for q in statistics.quantiles(worker_average_respond_list, n=4)]

    frontend_server_percentile = [round(q, 3) for q in statistics.quantiles(frontend_average_responde_list, n=4)]
    # Determines slow servers. Those above the 4th percentile are considered slow
    slow_worker_server = [server for server, average_time in worker_average_response_time.items() if average_time >= worker_server_percentile[2]]
    slow_frontend_server = [server for server, average_time in frontend_average_response_time.items() if average_time >= frontend_server_percentile[2]]

    return slow_worker_server, slow_frontend_server

slow_worker, slow_frontend = slow_server_finder(log_file)

print("Slow worker servers: ", slow_worker)
print("Slow frontend servers: ", slow_frontend)














