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


def get_login_job_by_id(login_job_id):
    for job in LOGIN_JOB.values():
        id_ = job[0]
        if login_job_id == id_:
            return job
    return None


def is_zero(job_id):
    return job_id == 10000 or job_id == 10100 or job_id == 10110 or job_id == 10111 or job_id == 10112


def is_xenon(job_id):
    return job_id // 100 == 36 or job_id == 3002


def is_demon(job_id):
    return job_id // 100 == 31 or job_id == 3001


def is_beast_tamer(job_id):
    return job_id // 1000 == 11


def is_pink_bean(job_id):
    return job_id == 13000 or job_id == 13100


def is_manager(job_id):
    return job_id == 800


def gm(job_id):
    return job_id == JobEnum.GM.value[0]


def is_super_gm(job_id):
    return job_id == JobEnum.SUPERGM.value[0]


def is_gm_job(job_id):
    return gm(job_id) or is_super_gm(job_id)


def is_extend_sp_job(job_id):
    return not is_beast_tamer(job_id) and not is_pink_bean(job_id) and not is_gm_job(job_id) and not is_manager(job_id)


def encode(out_packet: Packet):
    out_packet.encode_byte(ENABLE_JOBS)
    out_packet.encode_byte(JOB_ORDER)
    for job_info in LOGIN_JOB.values():
        job_type = job_info[0]
        job_flag = job_info[1]
        job_enum = job_info[2]
        out_packet.encode_byte(job_flag.value)
        out_packet.encode_short(job_flag.value)
