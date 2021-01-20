from src.net.enum.job_enum import JobFlag, JobEnum
from src.net.packets.byte_buffer.packet import Packet

ENABLE_JOBS = True
JOB_ORDER = 8

LOGIN_JOB = {
    # JobType, JobFlag, JobEnum
    'RESISTANCE': [
        0, JobFlag.ENABLED, JobEnum.CITIZEN
    ],
    'EXPLORER': [
        1, JobFlag.ENABLED, JobEnum.BEGINNER
    ],
    'CYGNUS': [
        2, JobFlag.ENABLED, JobEnum.NOBLESSE
    ],
    'ARAN': [
        3, JobFlag.ENABLED, JobEnum.LEGEND
    ],
    'EVAN': [
        4, JobFlag.ENABLED, JobEnum.EVAN_NOOB
    ],
    'MERCEDES': [
        5, JobFlag.ENABLED, JobEnum.MERCEDES
    ],
    'DEMON': [
        6, JobFlag.ENABLED, JobEnum.DEMON_SLAYER
    ],
    'PHANTOM': [
        7, JobFlag.ENABLED, JobEnum.PHANTOM
    ],
    'DUAL_BLADE': [
        8, JobFlag.ENABLED, JobEnum.BEGINNER
    ],
    'MIHILE': [
        9, JobFlag.ENABLED, JobEnum.NAMELESS_WARDEN
    ],
    'LUMINOUS': [
        10, JobFlag.ENABLED, JobEnum.LUMINOUS
    ],
    'KAISER': [
        11, JobFlag.ENABLED, JobEnum.KAISER
    ],
    'ANGELIC': [
        12, JobFlag.ENABLED, JobEnum.ANGELIC_BUSTER
    ],
    'CANNONER': [
        13, JobFlag.ENABLED, JobEnum.BEGINNER
    ],
    'XENON': [
        14, JobFlag.ENABLED, JobEnum.XENON
    ],
    'ZERO': [
        15, JobFlag.ENABLED, JobEnum.ZERO
    ],
    'SHADE': [
        16, JobFlag.ENABLED, JobEnum.SHADE
    ],
    'JETT': [
        17, JobFlag.ENABLED, JobEnum.BEGINNER
    ],
    'HAYATO': [
        18, JobFlag.ENABLED, JobEnum.HAYATO
    ],
    'KANNA': [
        19, JobFlag.ENABLED, JobEnum.KANNA
    ],
    'CHASE': [
        20, JobFlag.ENABLED, JobEnum.BEAST_TAMER
    ],
    'PINK_BEAN': [
        21, JobFlag.ENABLED, JobEnum.PINK_BEAN_0
    ],
    'KINESIS': [
        22, JobFlag.ENABLED, JobEnum.KINESIS_0
    ],
}


def encode(out_packet: Packet):
    out_packet.encode_byte(ENABLE_JOBS)
    out_packet.encode_byte(JOB_ORDER)
    for job_info in LOGIN_JOB.values():
        job_type = job_info[0]
        job_flag = job_info[1]
        job_enum = job_info[2]
        out_packet.encode_byte(job_flag.value)
        out_packet.encode_byte(job_flag.value)
