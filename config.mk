
# DEFAULT 
DDR_MEM ?= 0x80000000

#ETHERNET PATHS
ETHERNET_HW_DIR:=$(ETHERNET_DIR)/hardware
ETHERNET_INC_DIR:=$(ETHERNET_HW_DIR)/include
ETHERNET_SRC_DIR:=$(ETHERNET_HW_DIR)/src
ETHERNET_FPGA_DIR:=$(ETHERNET_DIR)/fpga
ETHERNET_SW_DIR:=$(ETHERNET_DIR)/software
ETHERNET_PYTHON_DIR=$(ETHERNET_SW_DIR)/python
SIM_DIR ?=$(ETHERNET_HW_DIR)/simulation/$(SIMULATOR)
ETHERNET_TB_DIR:=$(ETHERNET_HW_DIR)/testbench
SUBMODULES_DIR:=$(ETHERNET_DIR)/submodules

# SUBMODULE PATHS
LIB_DIR ?=$(ETHERNET_DIR)/submodules/LIB
MEM_DIR ?=$(ETHERNET_DIR)/submodules/MEM
AXI_DIR ?=$(ETHERNET_DIR)/submodules/AXI

SIMULATOR ?=icarus

#DEFAULT FPGA FAMILY
FPGA_FAMILY ?=CYCLONEV-GT
FPGA_FAMILY_LIST ?=CYCLONEV-GT XCKU

#DEFAULT DOC
DOC ?=pb
DOC_LIST ?=pb ug

# VERSION
VERSION ?=V0.1
iob_eth_version.txt:
	echo $(VERSION) > version.txt
