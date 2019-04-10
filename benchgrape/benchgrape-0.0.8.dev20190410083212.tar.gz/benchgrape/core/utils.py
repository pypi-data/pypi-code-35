
def map_benchmark_data(raw_data):
    """"
    map benchmark data do internal format -> currently just a proxy where
    we could interfere
    :param raw_data: ``dict``
    :return: ``dict``
    """
    organization = raw_data['organization']
    organization['url'] = raw_data['url']

    users = []
    for id, user_data in raw_data['users'].items():
        meta = user_data
        meta['id'] = id
        users.append(meta)

    groups = []
    for id, group_data in raw_data['groups'].items():
        meta = group_data
        meta['id'] = id
        groups.append(meta)

    pcs = []
    for id, pc_data in raw_data['private_conversations'].items():
        meta = pc_data
        meta['id'] = id
        pcs.append(meta)

    return organization, users, groups, pcs

    # import subprocess, time, os, sys
    #
    # cmd = "rsync.exe -vaz souce/ dest/"
    #
    # p = subprocess.Popen(cmd,
    #                      shell=True,
    #                      bufsize=64,
    #                      stdin=subprocess.PIPE,
    #                      stderr=subprocess.PIPE,
    #                      stdout=subprocess.PIPE)
    #
    # for line in p.stdout:
    #     print(">>> " + str(line.rstrip()))
    #     p.stdout.flush()
    #

#
# seek = 0
# line = ""
# extra_run = 5000  ## rsync.exe send returncode before terminated. Extra bytes.
# while True:
#     self.std.seek(seek)
#     byte = str(self.std.read(1), "windows-1252")
#     if byte == "\n" or byte == "\r":
#         print(line)
#         line = ""
#     else:
#         line += byte
#     seek += 1
