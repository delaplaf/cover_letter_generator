import time
from typing import Any, Dict

from read_cv import load_pdf
from read_linkedin_job import extract_data_from_url


def generate_cover_letter(
    data: Dict[str, Any], model_parameters: Dict[str, Any]
) -> str:
    time.sleep(2)

    url = (
        r"https://www.linkedin.com/jobs/view/3720693103/"
        r"?alternateChannel=search&refId=Ot2vLR9dlvhIFMDob0MYBQ%3D%"
        r"3D&trackingId=yLPZnrcB%2BiqLioIipdVgsA%3D%3D"
    )

    cv = load_pdf(r"data\linkedin_cv.pdf")
    linkedin_data = extract_data_from_url(url)

    text = f"""
    ########## Job title ##########
    {linkedin_data["job_title"]}

    ########## Company Info ##########
    {linkedin_data["company_info"]}

    ########## Job description ##########
    {linkedin_data["job_description"]}

    ########## CV ##########
    {cv}
    """
    print(text)
    return text
