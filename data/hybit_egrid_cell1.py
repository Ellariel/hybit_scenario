'''

This file generates the pandapower-grid of the region around the Steel Plant in Bremen.
It includes busses for Wind Turbines and PV-Systems that are possibly added in the future.

Description: hybit_egrid_cell1.pdf
Grid file: hybit_egrid_cell1.json
Authors: Kaja Petersen <kaja.petersen@uni-oldenburg.de>

'''

import os
import argparse
import pandapower as pp

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


def make_grid_model(**kwargs):
        base_dir = kwargs.get('dir', './')
        verbose = kwargs.get('verbose', 1)

        #data_dir = os.path.join(base_dir, 'data')
        os.makedirs(base_dir, exist_ok=True)
        grid_file = os.path.join(base_dir, 'hybit_egrid_cell1.json')

        net = pp.create_empty_network(name="empty")

        # busses 380 kV - transmission network
        transb01 = pp.create_bus(net, vn_kv=380., name="transb1-substation Niedervieland")

        # busses 110 kV - high voltage distribution network
        hvb01 = pp.create_bus(net, vn_kv=110., name="hvb01-switchgear Grambke")
        hvb02 = pp.create_bus(net, vn_kv=110., name="hvb02-connection point Mittelsbueren")
        hvb03 = pp.create_bus(net, vn_kv=110., name="hvb03-Mittelsbueren")
        hvb04 = pp.create_bus(net, vn_kv=110., name="hvb04-connection point Niedervieland")
        hvb05 = pp.create_bus(net, vn_kv=110., name="hvb05-WT5")
        hvb06 = pp.create_bus(net, vn_kv=110., name="hvb06-WT6")
        hvb07 = pp.create_bus(net, vn_kv=110., name="hvb07-WT7")
        hvb08 = pp.create_bus(net, vn_kv=110., name="hvb08-WT8")
        hvb09 = pp.create_bus(net, vn_kv=110., name="hvb09-WT9")
        hvb10 = pp.create_bus(net, vn_kv=110., name="hvb10-WT10")
        hvb11 = pp.create_bus(net, vn_kv=110., name="hvb11-WT11")
        hvb12 = pp.create_bus(net, vn_kv=110., name="hvb12-WT12")
        hvb13 = pp.create_bus(net, vn_kv=110., name="hvb13-WT13")
        hvb14 = pp.create_bus(net, vn_kv=110., name="hvb14-WT14")
        hvb15 = pp.create_bus(net, vn_kv=110., name="hvb15-WT15")
        hvb16 = pp.create_bus(net, vn_kv=110., name="hvb16-WT16")
        hvb17 = pp.create_bus(net, vn_kv=110., name="hvb17-connection WP Stahlwerk")
        hvb18 = pp.create_bus(net, vn_kv=110., name="hvb18-WT22")
        hvb19 = pp.create_bus(net, vn_kv=110., name="hvb19-WT23")
        hvb20 = pp.create_bus(net, vn_kv=110., name="hvb20-WT24")
        hvb21 = pp.create_bus(net, vn_kv=110., name="hvb21-WT25")
        hvb22 = pp.create_bus(net, vn_kv=110., name="hvb22-WT26")
        hvb23 = pp.create_bus(net, vn_kv=110., name="hvb23-WT27")
        hvb24 = pp.create_bus(net, vn_kv=110., name="hvb24-WT28")
        hvb25 = pp.create_bus(net, vn_kv=110., name="hvb25-WT29")

        hvb26 = pp.create_bus(net, vn_kv=110., name="hvb26-Elektrolyseur")
        hvb27 = pp.create_bus(net, vn_kv=110., name="hvb27-Battery")

        # busses 20 kV - medium voltage distribution network
        ## it's only given, that the (wind) power plants are connected to medium voltage - don't know how to find out the exact voltage level
        mvb01 = pp.create_bus(net, vn_kv=20., name="mvb01-switchgear Grambke")
        mvb02 = pp.create_bus(net, vn_kv=20., name="mvb02-WT1-Forschungs WEA Bremen GmbH")
        mvb03 = pp.create_bus(net, vn_kv=20., name="mvb03-WT2-WP Powerwind Anlage 1")
        mvb04 = pp.create_bus(net, vn_kv=20., name="mvb04-WT3-WP Industriehaefen Anlage 1")
        mvb05 = pp.create_bus(net, vn_kv=20., name="mvb05-WT4-WP Industriehaefen Anlage 2")
        mvb06 = pp.create_bus(net, vn_kv=20., name="mvb06-WT17-WP Mittelsbueren")
        mvb07 = pp.create_bus(net, vn_kv=20., name="mvb07-WT18-WP Mittelsbueren")
        mvb08 = pp.create_bus(net, vn_kv=20., name="mvb08-WT19-Oelhafen")
        mvb09 = pp.create_bus(net, vn_kv=20., name="mvb09-WT20-WP Weserufer WEA 1")
        mvb10 = pp.create_bus(net, vn_kv=20., name="mvb10-WT21-WP Huettenstraße")
        mvb11a = pp.create_bus(net, vn_kv=20., name="mvb11a-SteelPlant")
        mvb11b = pp.create_bus(net, vn_kv=20., name="mvb11b-SteelPlant")
        mvb11c = pp.create_bus(net, vn_kv=20., name="mvb11c-SteelPlant")
        mvb11d = pp.create_bus(net, vn_kv=20., name="mvb11d-SteelPlant")

        #mvb11 = pp.create_bus(net, vn_kv=20., name="mvb11-Elektro-Lichtbogenofen")
        #mvb12 = pp.create_bus(net, vn_kv=20., name="mvb12-Direktreduktionsanlage")
        #mvb13 = pp.create_bus(net, vn_kv=20., name="mvb13-Warmwalzwerk")
        #mvb14 = pp.create_bus(net, vn_kv=20., name="mvb14-Kaltwalzwerk")
        #mvb15 = pp.create_bus(net, vn_kv=20., name="mvb15-Luftzerlegungsanlage")
        #mvb16 = pp.create_bus(net, vn_kv=20., name="mvb16-Verzinkereien")

        mvb12 = pp.create_bus(net, vn_kv=20., name="mvb12-Mittelsbüren")
        mvb14 = pp.create_bus(net, vn_kv=20., name="mvb14-Battery")

        mvb15 = pp.create_bus(net, vn_kv=20., name="mvb15-PV07")
        mvb16 = pp.create_bus(net, vn_kv=20., name="mvb16-PV10")
        # transformers for PVs
        mvb18 = pp.create_bus(net, vn_kv=20., name="mvb18-TransformerA")
        mvb19 = pp.create_bus(net, vn_kv=20., name="mvb19-TransformerB")
        mvb20 = pp.create_bus(net, vn_kv=20., name="mvb20-TransformerC")
        mvb21 = pp.create_bus(net, vn_kv=20., name="mvb21-TransformerD")
        mvb22 = pp.create_bus(net, vn_kv=20., name="mvb22-TransformerE")
        mvb23 = pp.create_bus(net, vn_kv=20., name="mvb23-TransformerF")
        mvb24 = pp.create_bus(net, vn_kv=20., name="mvb24-TransformerG")
        mvb25 = pp.create_bus(net, vn_kv=20., name="mvb25-TransformerH")
        # additional PVs
        mvb26 = pp.create_bus(net, vn_kv=20., name="mvb26-aPV.A1")
        mvb27 = pp.create_bus(net, vn_kv=20., name="mvb27-aPV.A2")
        mvb28 = pp.create_bus(net, vn_kv=20., name="mvb28-aPV.C3")
        mvb29 = pp.create_bus(net, vn_kv=20., name="mvb29-aPV.C4")
        mvb30 = pp.create_bus(net, vn_kv=20., name="mvb30-aPV.D4")
        # transformers for additional PVs
        mvb31 = pp.create_bus(net, vn_kv=20., name="mvb31-Transformer-aA1")
        mvb32 = pp.create_bus(net, vn_kv=20., name="mvb32-Transformer-aC1")
        mvb33 = pp.create_bus(net, vn_kv=20., name="mvb33-Transformer-aC2")
        mvb34 = pp.create_bus(net, vn_kv=20., name="mvb34-Transformer-aD1")
        mvb35 = pp.create_bus(net, vn_kv=20., name="mvb35-Transformer-aD2")
        mvb36 = pp.create_bus(net, vn_kv=20., name="mvb36-Transformer-aD3")
        mvb37 = pp.create_bus(net, vn_kv=20., name="mvb37-Transformer-aE1")
        mvb38 = pp.create_bus(net, vn_kv=20., name="mvb38-Transformer-aE2")
        mvb39 = pp.create_bus(net, vn_kv=20., name="mvb39-Transformer-aI1")
        mvb40 = pp.create_bus(net, vn_kv=20., name="mvb40-Transformer-aIJ")

        # busses 0.4 V - low voltage distribution network
        lvb001 = pp.create_bus(net, vn_kv=0.4, name="lvb001-TransformerA")
        lvb002 = pp.create_bus(net, vn_kv=0.4, name="lvb002-TransformerB")
        lvb003 = pp.create_bus(net, vn_kv=0.4, name="lvb003-TransformerC")
        lvb004 = pp.create_bus(net, vn_kv=0.4, name="lvb004-TransformerD")
        lvb005 = pp.create_bus(net, vn_kv=0.4, name="lvb005-TransformerE")
        lvb006 = pp.create_bus(net, vn_kv=0.4, name="lvb006-TransformerF")
        lvb007 = pp.create_bus(net, vn_kv=0.4, name="lvb007-TransformerG")
        lvb008 = pp.create_bus(net, vn_kv=0.4, name="lvb008-TransformerH")

        lvb009 = pp.create_bus(net, vn_kv=0.4, name="lvb009-PV01")
        lvb010 = pp.create_bus(net, vn_kv=0.4, name="lvb010-PV02")
        lvb011 = pp.create_bus(net, vn_kv=0.4, name="lvb011-PV03")
        lvb012 = pp.create_bus(net, vn_kv=0.4, name="lvb012-PV04")
        lvb013 = pp.create_bus(net, vn_kv=0.4, name="lvb013-PV05")
        lvb014 = pp.create_bus(net, vn_kv=0.4, name="lvb014-PV06")
        lvb015 = pp.create_bus(net, vn_kv=0.4, name="lvb015-PV08")
        lvb016 = pp.create_bus(net, vn_kv=0.4, name="lvb016-PV09")
        lvb017 = pp.create_bus(net, vn_kv=0.4, name="lvb017-PV11")
        lvb018 = pp.create_bus(net, vn_kv=0.4, name="lvb018-PV12")
        lvb019 = pp.create_bus(net, vn_kv=0.4, name="lvb019-PV13")
        lvb020 = pp.create_bus(net, vn_kv=0.4, name="lvb020-PV14")
        lvb021 = pp.create_bus(net, vn_kv=0.4, name="lvb021-PV15")
        lvb022 = pp.create_bus(net, vn_kv=0.4, name="lvb022-PV16")
        lvb023 = pp.create_bus(net, vn_kv=0.4, name="lvb023-PV17")
        lvb024 = pp.create_bus(net, vn_kv=0.4, name="lvb024-PV18")
        lvb025 = pp.create_bus(net, vn_kv=0.4, name="lvb025-PV19")
        lvb026 = pp.create_bus(net, vn_kv=0.4, name="lvb026-PV20")
        lvb027 = pp.create_bus(net, vn_kv=0.4, name="lvb027-PV21")

        # transformers for additional PVs
        lvb028 = pp.create_bus(net, vn_kv=0.4, name="lvb028-Transformer-aA1")
        lvb029 = pp.create_bus(net, vn_kv=0.4, name="lvb029-Transformer-aC1")
        lvb030 = pp.create_bus(net, vn_kv=0.4, name="lvb030-Transformer-aC2")
        lvb031 = pp.create_bus(net, vn_kv=0.4, name="lvb031-Transformer-aD1")
        lvb032 = pp.create_bus(net, vn_kv=0.4, name="lvb032-Transformer-aD2")
        lvb033 = pp.create_bus(net, vn_kv=0.4, name="lvb033-Transformer-aD3")
        lvb034 = pp.create_bus(net, vn_kv=0.4, name="lvb034-Transformer-aE1")
        lvb035 = pp.create_bus(net, vn_kv=0.4, name="lvb035-Transformer-aE2")
        lvb036 = pp.create_bus(net, vn_kv=0.4, name="lvb036-Transformer-aI1")
        lvb037 = pp.create_bus(net, vn_kv=0.4, name="lvb037-Transformer-aIJ")

        # additional PVs
        lvb039 = pp.create_bus(net, vn_kv=0.4, name="lvb039-aPV.A3")
        lvb040 = pp.create_bus(net, vn_kv=0.4, name="lvb040-aPV.A4")
        lvb041 = pp.create_bus(net, vn_kv=0.4, name="lvb041-aPV.A5")
        lvb042 = pp.create_bus(net, vn_kv=0.4, name="lvb042-aPV.A6")
        lvb043 = pp.create_bus(net, vn_kv=0.4, name="lvb043-aPV.C1")
        lvb044 = pp.create_bus(net, vn_kv=0.4, name="lvb044-aPV.C5")

        lvb045 = pp.create_bus(net, vn_kv=0.4, name="lvb045-aPV.C6")
        lvb046 = pp.create_bus(net, vn_kv=0.4, name="lvb046-aPV.C7")
        lvb047 = pp.create_bus(net, vn_kv=0.4, name="lvb047-aPV.C8")
        lvb048 = pp.create_bus(net, vn_kv=0.4, name="lvb048-aPV.C9")
        lvb049 = pp.create_bus(net, vn_kv=0.4, name="lvb049-aPV.C10")
        lvb050 = pp.create_bus(net, vn_kv=0.4, name="lvb050-aPV.C11")
        lvb051 = pp.create_bus(net, vn_kv=0.4, name="lvb051-aPV.C12")
        lvb052 = pp.create_bus(net, vn_kv=0.4, name="lvb052-aPV.C13")
        lvb053 = pp.create_bus(net, vn_kv=0.4, name="lvb053-aPV.C14")

        lvb054 = pp.create_bus(net, vn_kv=0.4, name="lvb054-aPV.C16")
        lvb055 = pp.create_bus(net, vn_kv=0.4, name="lvb055-aPV.C17")
        lvb056 = pp.create_bus(net, vn_kv=0.4, name="lvb056-aPV.C18")
        lvb057 = pp.create_bus(net, vn_kv=0.4, name="lvb057-aPV.C19")
        lvb058 = pp.create_bus(net, vn_kv=0.4, name="lvb058-aPV.C20")
        lvb059 = pp.create_bus(net, vn_kv=0.4, name="lvb059-aPV.C21")
        lvb060 = pp.create_bus(net, vn_kv=0.4, name="lvb060-aPV.C22")
        lvb061 = pp.create_bus(net, vn_kv=0.4, name="lvb061-aPV.C23")
        lvb062 = pp.create_bus(net, vn_kv=0.4, name="lvb062-aPV.C24")
        lvb063 = pp.create_bus(net, vn_kv=0.4, name="lvb063-aPV.C25")
        lvb064 = pp.create_bus(net, vn_kv=0.4, name="lvb064-aPV.C26")
        lvb065 = pp.create_bus(net, vn_kv=0.4, name="lvb065-aPV.C27")
        lvb066 = pp.create_bus(net, vn_kv=0.4, name="lvb066-aPV.C28")
        lvb067 = pp.create_bus(net, vn_kv=0.4, name="lvb067-aPV.C29")

        lvb068 = pp.create_bus(net, vn_kv=0.4, name="lvb068-aPV.D1")
        lvb069 = pp.create_bus(net, vn_kv=0.4, name="lvb069-aPV.D2")
        lvb070 = pp.create_bus(net, vn_kv=0.4, name="lvb070-aPV.D3")

        lvb071 = pp.create_bus(net, vn_kv=0.4, name="lvb071-aPV.D5")
        lvb072 = pp.create_bus(net, vn_kv=0.4, name="lvb072-aPV.D6")
        lvb073 = pp.create_bus(net, vn_kv=0.4, name="lvb073-aPV.D7")
        lvb074 = pp.create_bus(net, vn_kv=0.4, name="lvb074-aPV.D8")
        lvb075 = pp.create_bus(net, vn_kv=0.4, name="lvb075-aPV.D9")
        lvb076 = pp.create_bus(net, vn_kv=0.4, name="lvb076-aPV.D10")
        lvb077 = pp.create_bus(net, vn_kv=0.4, name="lvb077-aPV.D11")
        lvb078 = pp.create_bus(net, vn_kv=0.4, name="lvb078-aPV.D12")
        lvb079 = pp.create_bus(net, vn_kv=0.4, name="lvb079-aPV.D13")
        lvb080 = pp.create_bus(net, vn_kv=0.4, name="lvb080-aPV.D14")
        lvb081 = pp.create_bus(net, vn_kv=0.4, name="lvb081-aPV.D15")

        lvb082 = pp.create_bus(net, vn_kv=0.4, name="lvb082-aPV.D16")
        lvb083 = pp.create_bus(net, vn_kv=0.4, name="lvb083-aPV.D17")
        lvb084 = pp.create_bus(net, vn_kv=0.4, name="lvb084-aPV.D18")
        lvb085 = pp.create_bus(net, vn_kv=0.4, name="lvb085-aPV.D19")
        lvb086 = pp.create_bus(net, vn_kv=0.4, name="lvb086-aPV.D20")
        lvb087 = pp.create_bus(net, vn_kv=0.4, name="lvb087-aPV.D21")
        lvb088 = pp.create_bus(net, vn_kv=0.4, name="lvb088-aPV.D22")
        lvb089 = pp.create_bus(net, vn_kv=0.4, name="lvb089-aPV.D23")
        lvb090 = pp.create_bus(net, vn_kv=0.4, name="lvb090-aPV.D24")
        lvb091 = pp.create_bus(net, vn_kv=0.4, name="lvb091-aPV.D25")
        lvb092 = pp.create_bus(net, vn_kv=0.4, name="lvb092-aPV.D26")
        lvb093 = pp.create_bus(net, vn_kv=0.4, name="lvb093-aPV.D27")

        lvb094 = pp.create_bus(net, vn_kv=0.4, name="lvb094-aPV.E1")
        lvb095 = pp.create_bus(net, vn_kv=0.4, name="lvb095-aPV.E4")
        lvb096 = pp.create_bus(net, vn_kv=0.4, name="lvb096-aPV.E5")

        lvb097 = pp.create_bus(net, vn_kv=0.4, name="lvb097-aPV.E6")
        lvb098 = pp.create_bus(net, vn_kv=0.4, name="lvb098-aPV.E7")
        lvb099 = pp.create_bus(net, vn_kv=0.4, name="lvb099-aPV.E8")
        lvb100 = pp.create_bus(net, vn_kv=0.4, name="lvb100-aPV.E9")
        lvb101 = pp.create_bus(net, vn_kv=0.4, name="lvb101-aPV.E10")
        lvb102 = pp.create_bus(net, vn_kv=0.4, name="lvb102-aPV.E11")
        lvb103 = pp.create_bus(net, vn_kv=0.4, name="lvb103-aPV.E12")
        lvb104 = pp.create_bus(net, vn_kv=0.4, name="lvb104-aPV.E13")
        lvb105 = pp.create_bus(net, vn_kv=0.4, name="lvb105-aPV.E14")
        lvb106 = pp.create_bus(net, vn_kv=0.4, name="lvb106-aPV.E15")
        lvb107 = pp.create_bus(net, vn_kv=0.4, name="lvb107-aPV.E16")
        lvb108 = pp.create_bus(net, vn_kv=0.4, name="lvb108-aPV.E17")

        lvb109 = pp.create_bus(net, vn_kv=0.4, name="lvb109-aPV.I1")
        lvb110 = pp.create_bus(net, vn_kv=0.4, name="lvb110-aPV.I2")
        lvb111 = pp.create_bus(net, vn_kv=0.4, name="lvb111-aPV.I3")
        lvb112 = pp.create_bus(net, vn_kv=0.4, name="lvb112-aPV.I4")
        lvb113 = pp.create_bus(net, vn_kv=0.4, name="lvb113-aPV.I5")
        lvb114 = pp.create_bus(net, vn_kv=0.4, name="lvb114-aPV.I6")
        lvb115 = pp.create_bus(net, vn_kv=0.4, name="lvb115-aPV.I7")

        lvb116 = pp.create_bus(net, vn_kv=0.4, name="lvb116-aPV.I8")
        lvb117 = pp.create_bus(net, vn_kv=0.4, name="lvb117-aPV.I9")

        lvb118 = pp.create_bus(net, vn_kv=0.4, name="lvb118-aPV.J1")
        lvb119 = pp.create_bus(net, vn_kv=0.4, name="lvb119-aPV.J2")
        lvb120 = pp.create_bus(net, vn_kv=0.4, name="lvb120-aPV.J3")
        lvb121 = pp.create_bus(net, vn_kv=0.4, name="lvb121-aPV.J4")


        # lines
        ## standard types: https://pandapower.readthedocs.io/en/v2.13.1/std_types/basic.html#lines
        ## type: cs = cable; ol = overhead lines

        # overhead lines - 110 kV - real length
        ## So far simply selected one of the ten available standard types for 110 kV overhead lines
        ol_110kv_std_type = "48-AL1/8-ST1A 110.0"
        #ol_110kv_std_type = "70-AL1/11-ST1A 110.0"
        #ol_110kv_std_type = "94-AL1/15-ST1A 110.0"
        #ol_110kv_std_type = "122-AL1/20-ST1A 110.0"
        #ol_110kv_std_type = "149-AL1/24-ST1A 110.0"
        #ol_110kv_std_type = "184-AL1/30-ST1A 110.0"
        #ol_110kv_std_type = "243-AL1/39-ST1A 110.0"
        #ol_110kv_std_type = "305-AL1/39-ST1A 110.0"
        #ol_110kv_std_type = "490-AL1/64-ST1A 110.0"
        #ol_110kv_std_type = "679-AL1/86-ST1A 110.0"

        pp.create_line(net, hvb01, hvb02, std_type=ol_110kv_std_type, length_km=5.54, name="Freileitung Grambke-Mittelsbueren-Niedervieland part1")
        #pp.create_line(net, hvb01, hvb02, std_type=ol_110kv_std_type, length_km=5.54, name="Freileitung Grambke-Mittelsbueren-Niedervieland part1")
        pp.create_line(net, hvb02, hvb03, std_type=ol_110kv_std_type, length_km=1.75, name="Freileitung Grambke-Mittelsbueren-Niedervieland part2")
        #pp.create_line(net, hvb02, hvb03, std_type=ol_110kv_std_type, length_km=1.75, name="Freileitung Grambke-Mittelsbueren-Niedervieland part2")
        pp.create_line(net, hvb02, hvb04, std_type=ol_110kv_std_type, length_km=6.58, name="Freileitung Grambke-Mittelsbueren-Niedervieland part3")

        # high voltage cables - 110 kV
        ## So far simply selected one of the four available standard types for 110 kV cables
        #cs_110kv_std_type = "N2XS(FL)2Y 1x120 RM/35 64/110 kV"
        cs_110kv_std_type = "N2XS(FL)2Y 1x185 RM/35 64/110 kV"
        #cs_110kv_std_type = "N2XS(FL)2Y 1x240 RM/35 64/110 kV"
        #cs_110kv_std_type = "N2XS(FL)2Y 1x300 RM/35 64/110 kV"

        # Electrolyser
        #pp.create_line(net, hvb03, hvb26, std_type=cs_110kv_std_type, length_km=0.20, name="Mittelsbueren-Elektrolyseur") #LENGTH CHECK!!
        # assumed electrolyzer to be next to gas power plant Mittelbüren
        pp.create_line(net, hvb03, hvb26, std_type=cs_110kv_std_type, length_km=0.20, name="Mittelsbueren-Elektrolyseur") #LENGTH CHECK!!
        pp.create_line(net, hvb03, hvb27, std_type=cs_110kv_std_type, length_km=0.20, name="Mittelsbueren-Battery") #LENGTH CHECK!!

        # WP Weserwind - all lengths oriented at streets
        pp.create_line(net, hvb05, hvb07, std_type=cs_110kv_std_type, length_km=0.46, name="WT5-WT7_WP Weserwind")
        pp.create_line(net, hvb07, hvb10, std_type=cs_110kv_std_type, length_km=0.87, name="WT7-WT10_WP Weserwind")
        #pp.create_line(net, hvb07, hvb10, std_type=cs_110kv_std_type, length_km=1.33, name="WT7-Mittelsbueren_WP Weserwind")
        pp.create_line(net, hvb06, hvb08, std_type=cs_110kv_std_type, length_km=0.53, name="WT6-WT8_WP Weserwind")
        pp.create_line(net, hvb08, hvb10, std_type=cs_110kv_std_type, length_km=0.50, name="WT8-WT10_WP Weserwind")
        #pp.create_line(net, hvb08, hvb10, std_type=cs_110kv_std_type, length_km=0.96, name="WT8-Mittelsbueren_WP Weserwind")
        pp.create_line(net, hvb09, hvb10, std_type=cs_110kv_std_type, length_km=0.57, name="WT9-WT10_WP Weserwind")
        pp.create_line(net, hvb10, hvb03, std_type=cs_110kv_std_type, length_km=0.46, name="WT10-Mittelbueren_WP Weserwind")

        # WP Stahlwerk Bremen - all lengths oriented at streets
        pp.create_line(net, hvb11, hvb12, std_type=cs_110kv_std_type, length_km=0.45, name="WT11-WT12_WP Stahlwerk")
        pp.create_line(net, hvb12, hvb17, std_type=cs_110kv_std_type, length_km=0.51, name="WT12-connectionPoint_WP Stahlwerk")
        pp.create_line(net, hvb14, hvb13, std_type=cs_110kv_std_type, length_km=0.31, name="WT14-WR13_WP Stahlwerk")
        pp.create_line(net, hvb13, hvb17, std_type=cs_110kv_std_type, length_km=0.30, name="WT13-connectionPoint_WP Stahlwerk")
        pp.create_line(net, hvb15, hvb16, std_type=cs_110kv_std_type, length_km=0.61, name="WT15-WR16_WP Stahlwerk")
        pp.create_line(net, hvb16, hvb17, std_type=cs_110kv_std_type, length_km=1.24, name="WT16-connectionPoint_WP Stahlwerk")
        pp.create_line(net, hvb17, hvb03, std_type=cs_110kv_std_type, length_km=0.84, name="connectionPoint-Mittelsbueren_WP Stahlwerk ")

        # planned turbines - thought up locations, distances oriented at streets
            # phase 1
        #pp.create_line(net, hvb18, hvb19, std_type=cs_110kv_std_type, length_km=0.39, name="WT22-WT23_Phase1")
        pp.create_line(net, hvb18, hvb03, std_type=cs_110kv_std_type, length_km=1.62, name="WT22-Mittelsbueren_Phase1")
        #pp.create_line(net, hvb20, hvb19, std_type=cs_110kv_std_type, length_km=0.39, name="WT24-WT23_Phase1")
        pp.create_line(net, hvb20, hvb03, std_type=cs_110kv_std_type, length_km=1.62, name="WT24-WT23_Phase1")
        pp.create_line(net, hvb19, hvb03, std_type=cs_110kv_std_type, length_km=1.23, name="WT23-Mittelsbueren_Phase1")
            # phase 2
        pp.create_line(net, hvb21, hvb22, std_type=cs_110kv_std_type, length_km=0.21, name="WT25-WT26_Phase2")
        #pp.create_line(net, hvb21, hvb03, std_type=cs_110kv_std_type, length_km=3.73, name="WT25-Mittelsbueren_Phase2")
        pp.create_line(net, hvb22, hvb23, std_type=cs_110kv_std_type, length_km=0.52, name="WT26-WT27_Phase2")
        #pp.create_line(net, hvb22, hvb03, std_type=cs_110kv_std_type, length_km=3.52, name="WT26-Mittelsbueren_Phase2")
        pp.create_line(net, hvb23, hvb03, std_type=cs_110kv_std_type, length_km=3.0, name="WT27-Mittelsbueren_Phase2")
        pp.create_line(net, hvb24, hvb03, std_type=cs_110kv_std_type, length_km=1.5, name="WT28-Mittelsbueren_Phase2")
        pp.create_line(net, hvb25, hvb24, std_type=cs_110kv_std_type, length_km=0.38, name="WT29-WT28_Phase2")
        #pp.create_line(net, hvb25, hvb03, std_type=cs_110kv_std_type, length_km=1.88, name="WT29-Mittelsbueren_Phase2")

        # cables - 20 kV
        ## So far simply selected one of the six available standard types for 20 kV cables
        #cs_20kv_std_type = "NA2XS2Y 1x95 RM/25 12/20 kV"
        #cs_20kv_std_type = "NA2XS2Y 1x185 RM/25 12/20 kV"
        cs_20kv_std_type = "NA2XS2Y 1x240 RM/25 12/20 kV"
        #cs_20kv_std_type = "NA2XS2Y 1x150 RM/25 12/20 kV"
        #cs_20kv_std_type = "NA2XS2Y 1x120 RM/25 12/20 kV"
        #cs_20kv_std_type = "NA2XS2Y 1x70 RM/25 12/20 kV"

        # load
        #pp.create_line(net, mvb01, mvb11, std_type=cs_20kv_std_type, length_km=2, name="Grambke-SteelPlant")
        #pp.create_line(net, mvb01, mvb11, std_type=cs_20kv_std_type, length_km=, name="Grambke-Elektro-Lichtbogenofen")
        #pp.create_line(net, mvb01, mvb12, std_type=cs_20kv_std_type, length_km=, name="Grambke-Direktreduktionsanlage")
        pp.create_line(net, mvb01, mvb11a, std_type=cs_20kv_std_type, length_km=2, name="Grambke-SteelPlant") # length: as the crow flies
        pp.create_line(net, mvb01, mvb11b, std_type=cs_20kv_std_type, length_km=2, name="Grambke-SteelPlant") # length: as the crow flies
        pp.create_line(net, mvb01, mvb11c, std_type=cs_20kv_std_type, length_km=2, name="Grambke-Steelplant") # length: as the crow flies
        pp.create_line(net, mvb01, mvb11d, std_type=cs_20kv_std_type, length_km=2, name="Grambke-Steelplant") # length: as the crow flies
        #pp.create_line(net, mvb01, mvb15, std_type=cs_20kv_std_type, length_km=, name="Grambke-Luftzerlegungsanlage")
        #pp.create_line(net, mvb01, mvb16, std_type=cs_20kv_std_type, length_km=, name="Grambke-Verzinkereien")

        # assumed Battery to be located near the gas power plants
        pp.create_line(net, mvb01, mvb12, std_type=cs_20kv_std_type, length_km=2.5, name="Grambke-Mittelsbüren")
        pp.create_line(net, mvb12, mvb14, std_type=cs_20kv_std_type, length_km=0.1, name="Mittelsbüren-Battery")

        # wind turbines
        pp.create_line(net, mvb02, mvb01, std_type=cs_20kv_std_type, length_km=2.36, name="WT1-Grambke_Forschungs WEA") # length: as the crow flies
        pp.create_line(net, mvb03, mvb01, std_type=cs_20kv_std_type, length_km=2.37, name="WT2-Grambke_WP Powerwind") # length: as the crow flies
        pp.create_line(net, mvb04, mvb05, std_type=cs_20kv_std_type, length_km=0.74, name="WT3-WR4_WP Industriehaefen") # length: as the crow flies
        pp.create_line(net, mvb05, mvb01, std_type=cs_20kv_std_type, length_km=2.68, name="WT4-Grambke_WP Industriehaefen") # length: as the crow flies
        pp.create_line(net, mvb06, mvb07, std_type=cs_20kv_std_type, length_km=0.57, name="WT17-WR18_WP Mittelsbueren") # length: oriented at streets
        pp.create_line(net, mvb07, mvb01, std_type=cs_20kv_std_type, length_km=1.86, name="WT18-Grambke_WP Mittelsbueren") # length: oriented at streets
        pp.create_line(net, mvb08, mvb01, std_type=cs_20kv_std_type, length_km=1.02, name="WT19-Grambke_Oelhafen") # length: oriented at streets
        pp.create_line(net, mvb09, mvb01, std_type=cs_20kv_std_type, length_km=2.13, name="WT20-Grambke_WP Weserufer") # length: oriented at streets
        pp.create_line(net, mvb10, mvb01, std_type=cs_20kv_std_type, length_km=2.60, name="WT21-Grambke_WP Huettenstraße") # length: oriented at streets

        # pv panels
        pp.create_line(net, mvb15, mvb01, std_type=cs_20kv_std_type, length_km=1.45, name="PV07-Grambke") # length: oriented at streets
        pp.create_line(net, mvb16, mvb01, std_type=cs_20kv_std_type, length_km=0.98, name="PV10-Grambke") # length: oriented at streets
        # additional PVs
        pp.create_line(net, mvb26, mvb01, std_type=cs_20kv_std_type, length_km=3, name="aPV.A1-Grambke") # length: oriented at streets
        pp.create_line(net, mvb27, mvb01, std_type=cs_20kv_std_type, length_km=3, name="aPV.A2-Grambke") # length: oriented at streets
        pp.create_line(net, mvb28, mvb01, std_type=cs_20kv_std_type, length_km=3, name="aPV.C3-Grambke") # length: oriented at streets
        pp.create_line(net, mvb29, mvb01, std_type=cs_20kv_std_type, length_km=2.5, name="aPV.C4-Grambke") # length: oriented at streets
        pp.create_line(net, mvb30, mvb01, std_type=cs_20kv_std_type, length_km=2.7, name="aPV.D4-Grambke") # length: oriented at streets

        # transformers
        pp.create_line(net, mvb18, mvb01, std_type=cs_20kv_std_type, length_km=1.09, name="TransformerA-Grambke") # length: oriented at streets
        pp.create_line(net, mvb19, mvb01, std_type=cs_20kv_std_type, length_km=1.36, name="TransformerB-Grambke") # length: oriented at streets
        pp.create_line(net, mvb20, mvb01, std_type=cs_20kv_std_type, length_km=1.70, name="TransformerC-Grambke") # length: oriented at streets
        pp.create_line(net, mvb21, mvb01, std_type=cs_20kv_std_type, length_km=0.85, name="TransformerD-Grambke") # length: oriented at streets
        pp.create_line(net, mvb22, mvb01, std_type=cs_20kv_std_type, length_km=0.87, name="TransformerE-Grambke") # length: oriented at streets
        pp.create_line(net, mvb23, mvb01, std_type=cs_20kv_std_type, length_km=0.76, name="TransformerF-Grambke") # length: oriented at streets
        pp.create_line(net, mvb24, mvb01, std_type=cs_20kv_std_type, length_km=1.68, name="TransformerG-Grambke") # length: oriented at streets
        pp.create_line(net, mvb25, mvb01, std_type=cs_20kv_std_type, length_km=2.26, name="TransformerH-Grambke") # length: oriented at streets

        # transformers of additional pvs
        pp.create_line(net, mvb31, mvb01, std_type=cs_20kv_std_type, length_km=2.00, name="Transformer.aA1-Grambke") # length: oriented at streets
        pp.create_line(net, mvb32, mvb01, std_type=cs_20kv_std_type, length_km=2.34, name="Transformer.aC1-Grambke") # length: oriented at streets
        pp.create_line(net, mvb33, mvb01, std_type=cs_20kv_std_type, length_km=2.98, name="Transformer.aC2-Grambke") # length: oriented at streets
        pp.create_line(net, mvb34, mvb01, std_type=cs_20kv_std_type, length_km=2.11, name="Transformer.aD1-Grambke") # length: oriented at streets
        pp.create_line(net, mvb35, mvb01, std_type=cs_20kv_std_type, length_km=2.0, name="Transformer.aD2-Grambke") # length: oriented at streets
        pp.create_line(net, mvb36, mvb01, std_type=cs_20kv_std_type, length_km=1.63, name="Transformer.aD3-Grambke") # length: oriented at streets
        pp.create_line(net, mvb37, mvb01, std_type=cs_20kv_std_type, length_km=2.75, name="Transformer.aE1-Grambke") # length: oriented at streets
        pp.create_line(net, mvb38, mvb01, std_type=cs_20kv_std_type, length_km=2.49, name="Transformer.aE2-Grambke") # length: oriented at streets
        pp.create_line(net, mvb39, mvb01, std_type=cs_20kv_std_type, length_km=1.91, name="Transformer.aI1-Grambke") # length: oriented at streets
        pp.create_line(net, mvb40, mvb01, std_type=cs_20kv_std_type, length_km=2.17, name="Transformer.aIJ-Grambke") # length: oriented at streets

        # cables - 0.4 kV
        ## So far simply selected one of the four available standard types for 0.4 kV cables
        #cs_400v_std_type = "15-AL1/3-ST1A 0.4"
        #cs_400v_std_type = "24-AL1/4-ST1A 0.4"
        #cs_400v_std_type = "48-AL1/8-ST1A 0.4"
        cs_400v_std_type = "94-AL1/15-ST1A 0.4"

        # PV to transformers
        pp.create_line(net, lvb009, lvb001, std_type=cs_400v_std_type, length_km=0.25, name="PV01-TransformerA") # length: oriented at streets
        pp.create_line(net, lvb010, lvb002, std_type=cs_400v_std_type, length_km=0.38, name="PV02-TransformerB") # length: oriented at streets
        pp.create_line(net, lvb011, lvb002, std_type=cs_400v_std_type, length_km=0.17, name="PV03-TransformerB") # length: oriented at streets
        pp.create_line(net, lvb012, lvb003, std_type=cs_400v_std_type, length_km=0.09, name="PV04-TransformerC") # length: oriented at streets
        pp.create_line(net, lvb013, lvb002, std_type=cs_400v_std_type, length_km=0.53, name="PV05-TransformerB") # length: oriented at streets
        pp.create_line(net, lvb014, lvb001, std_type=cs_400v_std_type, length_km=0.13, name="PV06-TransformerA") # length: oriented at streets
        pp.create_line(net, lvb015, lvb004, std_type=cs_400v_std_type, length_km=0.08, name="PV08-TransformerD") # length: oriented at streets
        pp.create_line(net, lvb016, lvb005, std_type=cs_400v_std_type, length_km=0.25, name="PV09-TransformerE") # length: oriented at streets
        pp.create_line(net, lvb017, lvb005, std_type=cs_400v_std_type, length_km=0.33, name="PV11-TransformerE") # length: oriented at streets
        pp.create_line(net, lvb018, lvb005, std_type=cs_400v_std_type, length_km=0.37, name="PV12-TransformerE") # length: oriented at streets
        pp.create_line(net, lvb019, lvb006, std_type=cs_400v_std_type, length_km=0.08, name="PV13-TransformerF") # length: oriented at streets
        pp.create_line(net, lvb020, lvb007, std_type=cs_400v_std_type, length_km=0.16, name="PV14-TransformerG") # length: oriented at streets
        pp.create_line(net, lvb021, lvb002, std_type=cs_400v_std_type, length_km=0.13, name="PV15-TransformerB") # length: oriented at streets
        pp.create_line(net, lvb022, lvb002, std_type=cs_400v_std_type, length_km=0.38, name="PV16-TransformerB") # length: oriented at streets
        pp.create_line(net, lvb023, lvb008, std_type=cs_400v_std_type, length_km=0.20, name="PV17-TransformerH") # length: oriented at streets
        pp.create_line(net, lvb024, lvb006, std_type=cs_400v_std_type, length_km=0.08, name="PV18-TransformerF") # length: oriented at streets
        pp.create_line(net, lvb025, lvb002, std_type=cs_400v_std_type, length_km=0.08, name="PV19-TransformerB") # length: oriented at streets
        pp.create_line(net, lvb026, lvb001, std_type=cs_400v_std_type, length_km=0.25, name="PV20-TransformerA") # length: oriented at streets
        pp.create_line(net, lvb027, lvb004, std_type=cs_400v_std_type, length_km=0.25, name="PV21-TransformerD") # length: oriented at streets

        # additional PVs
        #aA1
        pp.create_line(net, lvb039, lvb028, std_type=cs_400v_std_type, length_km=0.18, name="aPV.A3-Transformer-aA1") # length: oriented at streets
        pp.create_line(net, lvb040, lvb028, std_type=cs_400v_std_type, length_km=0.07, name="aPV.A4-Transformer-aA1") # length: oriented at streets
        pp.create_line(net, lvb041, lvb028, std_type=cs_400v_std_type, length_km=0.05, name="aPV.A5-Transformer-aA1") # length: oriented at streets
        pp.create_line(net, lvb042, lvb028, std_type=cs_400v_std_type, length_km=0.17, name="aPV.A6-Transformer-aA1") # length: oriented at streets
        pp.create_line(net, lvb043, lvb028, std_type=cs_400v_std_type, length_km=0.80, name="aPV.C1-Transformer-aA1") # length: oriented at streets ## 800m is too long for 1. std-type
        #aC1
        pp.create_line(net, lvb044, lvb029, std_type=cs_400v_std_type, length_km=0.24, name="aPV.C5-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb045, lvb029, std_type=cs_400v_std_type, length_km=0.19, name="aPV.C6-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb046, lvb029, std_type=cs_400v_std_type, length_km=0.16, name="aPV.C7-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb047, lvb029, std_type=cs_400v_std_type, length_km=0.09, name="aPV.C8-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb048, lvb029, std_type=cs_400v_std_type, length_km=0.04, name="aPV.C9-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb049, lvb029, std_type=cs_400v_std_type, length_km=0.53, name="aPV.C10-Transformer-aC1") # length: oriented at streets ## too long for 1. std-type
        pp.create_line(net, lvb050, lvb029, std_type=cs_400v_std_type, length_km=0.19, name="aPV.C11-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb051, lvb029, std_type=cs_400v_std_type, length_km=0.31, name="aPV.C12-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb052, lvb029, std_type=cs_400v_std_type, length_km=0.57, name="aPV.C13-Transformer-aC1") # length: oriented at streets
        pp.create_line(net, lvb053, lvb029, std_type=cs_400v_std_type, length_km=0.57, name="aPV.C14-Transformer-aC1") # length: oriented at streets
        #aC2
        pp.create_line(net, lvb054, lvb030, std_type=cs_400v_std_type, length_km=0.17, name="aPV.C16-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb055, lvb030, std_type=cs_400v_std_type, length_km=0.25, name="aPV.C17-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb056, lvb030, std_type=cs_400v_std_type, length_km=0.41, name="aPV.C18-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb057, lvb030, std_type=cs_400v_std_type, length_km=0.29, name="aPV.C19-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb058, lvb030, std_type=cs_400v_std_type, length_km=0.32, name="aPV.C20-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb059, lvb030, std_type=cs_400v_std_type, length_km=0.19, name="aPV.C21-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb060, lvb030, std_type=cs_400v_std_type, length_km=0.16, name="aPV.C22-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb061, lvb030, std_type=cs_400v_std_type, length_km=0.08, name="aPV.C23-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb062, lvb030, std_type=cs_400v_std_type, length_km=0.03, name="aPV.C24-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb063, lvb030, std_type=cs_400v_std_type, length_km=0.35, name="aPV.C25-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb064, lvb030, std_type=cs_400v_std_type, length_km=0.35, name="aPV.C26-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb065, lvb030, std_type=cs_400v_std_type, length_km=0.43, name="aPV.C27-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb066, lvb030, std_type=cs_400v_std_type, length_km=0.46, name="aPV.C28-Transformer-aC2") # length: oriented at streets
        pp.create_line(net, lvb067, lvb030, std_type=cs_400v_std_type, length_km=0.52, name="aPV.C29-Transformer-aC2") # length: oriented at streets
        #aD1
        pp.create_line(net, lvb068, lvb031, std_type=cs_400v_std_type, length_km=0.24, name="aPV.D1-Transformer-aD1") # length: oriented at streets
        pp.create_line(net, lvb069, lvb031, std_type=cs_400v_std_type, length_km=0.13, name="aPV.D2-Transformer-aD1") # length: oriented at streets
        pp.create_line(net, lvb070, lvb031, std_type=cs_400v_std_type, length_km=0.11, name="aPV.D3-Transformer-aD1") # length: oriented at streets
        #aD2
        pp.create_line(net, lvb071, lvb032, std_type=cs_400v_std_type, length_km=0.08, name="aPV.D5-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb072, lvb032, std_type=cs_400v_std_type, length_km=0.14, name="aPV.D6-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb073, lvb032, std_type=cs_400v_std_type, length_km=0.24, name="aPV.D7-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb074, lvb032, std_type=cs_400v_std_type, length_km=0.16, name="aPV.D8-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb075, lvb032, std_type=cs_400v_std_type, length_km=0.15, name="aPV.D9-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb076, lvb032, std_type=cs_400v_std_type, length_km=0.17, name="aPV.D10-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb077, lvb032, std_type=cs_400v_std_type, length_km=0.25, name="aPV.D11-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb078, lvb032, std_type=cs_400v_std_type, length_km=0.21, name="aPV.D12-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb079, lvb032, std_type=cs_400v_std_type, length_km=0.31, name="aPV.D13-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb080, lvb032, std_type=cs_400v_std_type, length_km=0.35, name="aPV.D14-Transformer-aD2") # length: oriented at streets
        pp.create_line(net, lvb081, lvb032, std_type=cs_400v_std_type, length_km=0.34, name="aPV.D15-Transformer-aD2") # length: oriented at streets
        #aD3
        pp.create_line(net, lvb082, lvb033, std_type=cs_400v_std_type, length_km=0.12, name="aPV.D16-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb083, lvb033, std_type=cs_400v_std_type, length_km=0.13, name="aPV.D17-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb084, lvb033, std_type=cs_400v_std_type, length_km=0.15, name="aPV.D18-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb085, lvb033, std_type=cs_400v_std_type, length_km=0.12, name="aPV.D19-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb086, lvb033, std_type=cs_400v_std_type, length_km=0.13, name="aPV.D20-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb087, lvb033, std_type=cs_400v_std_type, length_km=0.14, name="aPV.D21-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb088, lvb033, std_type=cs_400v_std_type, length_km=0.15, name="aPV.D22-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb089, lvb033, std_type=cs_400v_std_type, length_km=0.06, name="aPV.D23-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb090, lvb033, std_type=cs_400v_std_type, length_km=0.14, name="aPV.D24-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb091, lvb033, std_type=cs_400v_std_type, length_km=0.18, name="aPV.D25-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb092, lvb033, std_type=cs_400v_std_type, length_km=0.14, name="aPV.D26-Transformer-aD3") # length: oriented at streets
        pp.create_line(net, lvb093, lvb033, std_type=cs_400v_std_type, length_km=0.21, name="aPV.D27-Transformer-aD3") # length: oriented at streets
        #aE1
        pp.create_line(net, lvb094, lvb034, std_type=cs_400v_std_type, length_km=0.38, name="aPV.E1-Transformer-aE1") # length: oriented at streets
        pp.create_line(net, lvb095, lvb034, std_type=cs_400v_std_type, length_km=0.26, name="aPV.E4-Transformer-aE1") # length: oriented at streets
        pp.create_line(net, lvb096, lvb034, std_type=cs_400v_std_type, length_km=0.37, name="aPV.E5-Transformer-aE1") # length: oriented at streets
        #aE2
        pp.create_line(net, lvb097, lvb035, std_type=cs_400v_std_type, length_km=0.05, name="aPV.E6-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb098, lvb035, std_type=cs_400v_std_type, length_km=0.18, name="aPV.E7-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb099, lvb035, std_type=cs_400v_std_type, length_km=0.27, name="aPV.E8-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb100, lvb035, std_type=cs_400v_std_type, length_km=0.43, name="aPV.E9-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb101, lvb035, std_type=cs_400v_std_type, length_km=0.30, name="aPV.E10-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb102, lvb035, std_type=cs_400v_std_type, length_km=0.25, name="aPV.E11-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb103, lvb035, std_type=cs_400v_std_type, length_km=0.38, name="aPV.E12-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb104, lvb035, std_type=cs_400v_std_type, length_km=0.53, name="aPV.E13-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb105, lvb035, std_type=cs_400v_std_type, length_km=0.47, name="aPV.E14-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb106, lvb035, std_type=cs_400v_std_type, length_km=0.46, name="aPV.E15-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb107, lvb035, std_type=cs_400v_std_type, length_km=0.40, name="aPV.E16-Transformer-aE2") # length: oriented at streets
        pp.create_line(net, lvb108, lvb035, std_type=cs_400v_std_type, length_km=0.59, name="aPV.E17-Transformer-aE2") # length: oriented at streets

        #aI1
        pp.create_line(net, lvb109, lvb036, std_type=cs_400v_std_type, length_km=0.13, name="aPV.I1-Transformer-aI1") # length: oriented at streets
        pp.create_line(net, lvb110, lvb036, std_type=cs_400v_std_type, length_km=0.16, name="aPV.I2-Transformer-aI1") # length: oriented at streets
        pp.create_line(net, lvb111, lvb036, std_type=cs_400v_std_type, length_km=0.20, name="aPV.I3-Transformer-aI1") # length: oriented at streets
        pp.create_line(net, lvb112, lvb036, std_type=cs_400v_std_type, length_km=0.20, name="aPV.I4-Transformer-aI1") # length: oriented at streets
        pp.create_line(net, lvb113, lvb036, std_type=cs_400v_std_type, length_km=0.06, name="aPV.I5-Transformer-aI1") # length: oriented at streets
        pp.create_line(net, lvb114, lvb036, std_type=cs_400v_std_type, length_km=0.08, name="aPV.I6-Transformer-aI1") # length: oriented at streets
        pp.create_line(net, lvb115, lvb036, std_type=cs_400v_std_type, length_km=0.09, name="aPV.I7-Transformer-aI1") # length: oriented at streets
        #aIJ
        pp.create_line(net, lvb116, lvb037, std_type=cs_400v_std_type, length_km=0.13, name="aPV.I8-Transformer-aIJ") # length: oriented at streets
        pp.create_line(net, lvb117, lvb037, std_type=cs_400v_std_type, length_km=0.20, name="aPV.I9-Transformer-aIJ") # length: oriented at streets
        pp.create_line(net, lvb118, lvb037, std_type=cs_400v_std_type, length_km=0.45, name="aPV.J1-Transformer-aIJ") # length: oriented at streets
        pp.create_line(net, lvb119, lvb037, std_type=cs_400v_std_type, length_km=0.40, name="aPV.J2-Transformer-aIJ") # length: oriented at streets
        pp.create_line(net, lvb120, lvb037, std_type=cs_400v_std_type, length_km=0.40, name="aPV.J3-Transformer-aIJ") # length: oriented at streets
        pp.create_line(net, lvb121, lvb037, std_type=cs_400v_std_type, length_km=0.22, name="aPV.J4-Transformer-aIJ") # length: oriented at streets
        # transformer
        ## standard types: https://pandapower.readthedocs.io/en/v2.13.1/std_types/basic.html#transformers
        ## selected the only standard type for Transformers that transforms from 380 to 110
        pp.create_transformer(net, hv_bus=transb01, lv_bus=hvb04, std_type="160 MVA 380/110 kV")
        ## simply selected one of the three available standard types that transform from 110 to 20 kV
        pp.create_transformer(net, hv_bus=hvb01, lv_bus=mvb01, std_type="40 MVA 110/20 kV") #mittelsbueren
        ## simply selected one of the three available standard types that transform from 20 to 0.4 kV
        pp.create_transformer(net, hv_bus=mvb18, lv_bus=lvb001, std_type="0.4 MVA 20/0.4 kV") # transformerA
        pp.create_transformer(net, hv_bus=mvb19, lv_bus=lvb002, std_type="0.4 MVA 20/0.4 kV") # transformerB
        pp.create_transformer(net, hv_bus=mvb20, lv_bus=lvb003, std_type="0.4 MVA 20/0.4 kV") # transformerC
        pp.create_transformer(net, hv_bus=mvb21, lv_bus=lvb004, std_type="0.4 MVA 20/0.4 kV") # transformerD
        pp.create_transformer(net, hv_bus=mvb22, lv_bus=lvb005, std_type="0.4 MVA 20/0.4 kV") # transformerE
        pp.create_transformer(net, hv_bus=mvb23, lv_bus=lvb006, std_type="0.4 MVA 20/0.4 kV") # transformerF
        pp.create_transformer(net, hv_bus=mvb24, lv_bus=lvb007, std_type="0.4 MVA 20/0.4 kV") # transformerG
        pp.create_transformer(net, hv_bus=mvb25, lv_bus=lvb008, std_type="0.4 MVA 20/0.4 kV") # transformerH
        #additional PVs
        pp.create_transformer(net, hv_bus=mvb31, lv_bus=lvb028, std_type="0.4 MVA 20/0.4 kV") # transformer-aA1
        pp.create_transformer(net, hv_bus=mvb32, lv_bus=lvb029, std_type="0.4 MVA 20/0.4 kV") # transformer-aC1
        pp.create_transformer(net, hv_bus=mvb33, lv_bus=lvb030, std_type="0.4 MVA 20/0.4 kV") # transformer-aC2
        pp.create_transformer(net, hv_bus=mvb34, lv_bus=lvb031, std_type="0.4 MVA 20/0.4 kV") # transformer-aD1
        pp.create_transformer(net, hv_bus=mvb35, lv_bus=lvb032, std_type="0.4 MVA 20/0.4 kV") # transformer-aD2
        pp.create_transformer(net, hv_bus=mvb36, lv_bus=lvb033, std_type="0.4 MVA 20/0.4 kV") # transformer-aD3
        pp.create_transformer(net, hv_bus=mvb37, lv_bus=lvb034, std_type="0.4 MVA 20/0.4 kV") # transformer-aE1
        pp.create_transformer(net, hv_bus=mvb38, lv_bus=lvb035, std_type="0.4 MVA 20/0.4 kV") # transformer-aE2
        pp.create_transformer(net, hv_bus=mvb39, lv_bus=lvb036, std_type="0.4 MVA 20/0.4 kV") # transformer-aI1
        pp.create_transformer(net, hv_bus=mvb40, lv_bus=lvb037, std_type="0.4 MVA 20/0.4 kV") # transformer-aIJ


        # external grid
        ## external high voltage (380 kV) grid; connection point Niedervieland
        pp.create_ext_grid(net, bus=transb01, name="ExternalGrid")
        #pp.create_ext_grid(net, bus=hvb02, name="external grid")


        # generators
        ## not needed, generators added as simulators in the mosaik-scenario
        #pp.create_gen(net,bus=b3, p_mw = 0) # netto power of KW (according to Marktstammdatenregister: https://www.marktstammdatenregister.de/MaStR/Einheit/Detail/IndexOeffentlich/4443193)
        '''
        for i, g in net.bus.iterrows():
                if 'PV' in g['name'] or 'WT' in g['name']:
                        pp.create_sgen(net, i, p_mw=0.1, name=f"{g['name']}-StaticGen-{i}")
        '''

        # loads
        #example: #pp.create_load(net, bus=b3, p_mw=0.1, q_mvar=0.05)
        '''
        for i, g in net.bus.iterrows():
                if 'SteelPlant' in g['name']: # steel plan load just the first one
                        pp.create_load(net, i, p_mw=1.0, q_mvar=0.5, name=f"{g['name']}-Load-{i}")
                        #break
        '''
        
        net.bus['name'] = [f'{j}-Bus-{i}' for i, j in enumerate(net.bus['name'])]

        pp.runpp(net, numba=False)
        pp.to_json(net, grid_file)
        
        if verbose:
                print("buses", net.bus)
                print("lines", net.line)
                print("loads", net.load)
                print("sgens", net.sgen)
                print("trafos", net.trafo)
                print("ext_grid", net.ext_grid)

                print(f"Grid model of {len(net.bus)} buses, \
{len(net.line)} lines, \
{len(net.load)} loads, \
{len(net.sgen)} sgens, \
{len(net.trafo)} trafos, \
{len(net.ext_grid)} ext_grids")

                print(f"Grid model was saved: {grid_file}")



if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument('--dir', default=None, type=str)
        parser.add_argument('--verbose', default=1, type=int)
        args = parser.parse_args()
        
        if args.dir == None:
                args.dir = os.path.dirname(__file__)
                print('dir:', args.dir)
        
        make_grid_model(**vars(args))