"""ethBase.py

Base functions for socket communication with board.
"""
from socket import socket, AF_PACKET, AF_UNIX, SOCK_RAW, SOCK_SEQPACKET, htons, timeout
import time
import sys
import os

def PrintBaseUsage():
    print("<usage>: python eth_comm.py <interface> <RMAC> <file path>")

#Check arguments common to all scripts
if len(sys.argv) < 4:
    PrintBaseUsage()
    sys.exit()

addr = "/tmp/tmpLocalSocket"

#Ethernet parameters
interface = sys.argv[1]
# use byte arrays by default
src_addr = bytes.fromhex(sys.argv[2])       # sender MAC address
dst_addr = bytes.fromhex("01606e11020f")    # receiver MAC address
eth_type = bytes.fromhex("6000")            # ethernet frame type
ETH_P_ALL = 0x6000  

#Frame parameters
ETH_NBYTES = 1500
ETH_MINIMUM_NBYTES = (64-18)

#Frame header
ETH_HEADER = dst_addr + src_addr + eth_type

TIMEOUT = 0.1

#Open socket and bind
def CreateSocket():
    """
    Create raw socket. If "PC" is defined in the environment, creates an AF_UNIX
    socket instead.

    returns: socket object
    """
    if "PC" in os.environ:
        s = socket(AF_UNIX, SOCK_SEQPACKET)
        while True:
            try:
                s.connect(addr)
                break
            except:
                pass
    else:
        s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL))
        s.bind((interface, 0))

    s.settimeout(None)

    return s

def FormPacket(payload):
    """ 
    Generate packet from payload. Add padding to ensure minimum ethernet 
    packet size.

    payload: byte array with payload data

    return: byte array with {Eth header + payload + (optional padding)}
    """

    length = len(payload)
    if(length < ETH_MINIMUM_NBYTES):
        payload = payload + (b'\x00' * (ETH_MINIMUM_NBYTES - length))


    return ETH_HEADER + payload

def SendAndAck(socket,payload):
    """ 
    Send payload and receive acknowledge with same data.

    socket: socket for communication
    payload: bytes data payload
    return: difference count between send and received data
    """
    packet = FormPacket(payload)

    prev_timeout = socket.gettimeout()
    socket.settimeout(TIMEOUT)

    while True:
        bytes_sent = socket.send(packet)

        try:
            rcv = socket.recv(4096)
            break
        except timeout:
            pass

    socket.settimeout(prev_timeout)

    errors = 0
    for sent_byte, rcv_byte in zip(payload, rcv[len(ETH_HEADER):]):
        if sent_byte != rcv_byte:
            errors += 1

    return errors

def RcvAndAck(socket):   
    """ 
    Receive payload and send acknowledge with same data.

    socket: socket for communication
    return: received payload data (bytes)
    """
    rcv = socket.recv(4096)

    payload = rcv[len(ETH_HEADER):]

    socket.send(FormPacket(payload))

    return payload

def SyncAckFirst(socket):
    """ 
    Ping destination and wait for response at TIMEOUT intervals.

    socket: socket connection
    return: nothing
    """
    previous = socket.gettimeout()
    socket.settimeout(TIMEOUT)

    while True:
        socket.send(FormPacket(bytes('', encoding='ascii')))

        try:
            rcv = socket.recv(4096)
            break
        except timeout:
            pass

    socket.settimeout(previous)

def SyncAckLast(socket):
    """
    Wait for initial message from socket destination at TIMEOUT intervals.

    socket: socket connection
    return: nothing
    """
    previous = socket.gettimeout()
    socket.settimeout(TIMEOUT)

    while True:
        try:
            recv = socket.recv(4096)
            break
        except timeout:
            pass

    socket.send(FormPacket(bytes('', encoding='ascii')))

    socket.settimeout(previous)

# Print progress every so often 
def TimedPrintProgress(current,n_frames):
    """
    Print progress.

    current: current status.
    n_frames: total number of frames.
    return: nothing
    """
    TimedPrintProgress.storedMilli
    milli = int(round(time.time() * 1000))

    if(milli > (TimedPrintProgress.storedMilli + 100) or current == 0 or current == n_frames):
        print("\rProgress: %d / %d" % (current + 1,n_frames + 1))
        sys.stdout.flush()
        TimedPrintProgress.storedMilli = milli

TimedPrintProgress.storedMilli = 0
