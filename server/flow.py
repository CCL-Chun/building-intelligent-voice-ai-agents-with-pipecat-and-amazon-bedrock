#
# Copyright (c) 2024, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from loguru import logger

from pipecat_flows import FlowArgs, FlowConfig, FlowResult, FlowsFunctionSchema

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv(override=True)

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

# Flow Configuration - Travel Planner
#
# This configuration defines a vacation planning system with the following states:
#
# 1. start
#    - Initial state where user chooses between beach or mountain vacation
#    - Functions: choose_beach, choose_mountain
#    - Pre-action: Welcome message
#    - Transitions to: choose_beach or choose_mountain
#
# 2. choose_beach/choose_mountain
#    - Handles destination selection for chosen vacation type
#    - Functions:
#      * select_destination (node function with location-specific options)
#      * get_dates (transitions to date selection)
#    - Pre-action: Destination-specific welcome message
#
# 3. get_dates
#    - Handles travel date selection
#    - Functions:
#      * record_dates (node function, can be modified)
#      * get_activities (transitions to activity selection)
#
# 4. get_activities
#    - Handles activity preference selection
#    - Functions:
#      * record_activities (node function, array-based selection)
#      * verify_itinerary (transitions to verification)
#
# 5. verify_itinerary
#    - Reviews complete vacation plan
#    - Functions:
#      * revise_plan (loops back to get_dates)
#      * confirm_booking (transitions to confirmation)
#
# 6. confirm_booking
#    - Handles final confirmation and tips
#    - Functions: end
#    - Pre-action: Confirmation message
#
# 7. end
#    - Final state that closes the conversation
#    - No functions available
#    - Post-action: Ends conversation


# Type definitions
class DestinationResult(FlowResult):
    destination: str


class DatesResult(FlowResult):
    check_in: str
    check_out: str


class ActivitiesResult(FlowResult):
    activities: List[str]


# Function handlers
async def select_destination(args: FlowArgs) -> DestinationResult:
    """Handler for destination selection."""
    destination = args["destination"]
    # In a real app, this would store the selection
    return DestinationResult(destination=destination)


async def record_dates(args: FlowArgs) -> DatesResult:
    """Handler for travel date recording."""
    check_in = args["check_in"]
    check_out = args["check_out"]
    # In a real app, this would validate and store the dates
    return DatesResult(check_in=check_in, check_out=check_out)


async def record_activities(args: FlowArgs) -> ActivitiesResult:
    """Handler for activity selection."""
    activities = args["activities"]
    # In a real app, this would validate and store the activities
    return ActivitiesResult(activities=activities)

async def collect_requirements(args: FlowArgs) -> str:
    """Handler for collecting customer requirements."""
    # In a real app, this would validate and store the requirements
    requirements = args["requirements"]

    return True

async def check_willing(args: FlowArgs) -> bool:
    """Handler for checking customer's willingness to proceed."""
    willing = args["willing"]
    # In a real app, this would validate and store the willingness
    return willing


async def check_interest(args: FlowArgs) -> bool:
    """Handler for checking customer's interest in the product."""
    interest = args["interest"]
    # In a real app, this would validate and store the interest
    return interest

flow_config: FlowConfig = {
  "initial_node": "1_Start chat",
  "nodes": {
    "1_Start chat": {
      "task_messages": [
        {
          "role": "user",
          "content": """
          你現在正在與顧客進行通話，請先進行問候，並詢問對方最近的生活狀況。**不輸出語氣提示**"""
        }
      ],
      "functions": [
        {
          "type": "function",
          "function": {
            "name": "collect_requirements",
            "description": "Collect customer requirements",
            "parameters": {
              "type": "object",
              "properties": {
                "requirements": {
                  "type": "string",
                  "description": "Customer requirements"
                }
              }
            }
          }
        }
      ],
      "functions": [],
      "role_messages": [
        {
          "role": "system",
          "content": """
          你是一個 AI 銷售助理小森。你的個性就像是鄰居家中那個總是帶著溫暖笑容、親切有禮、真心關心長輩且非常孝順的年輕人。
          你說話真誠、語氣溫和，總是將對方的感受放在第一位。同時，你也是一位專業且值得信賴的銷售助理，
          你的目標是與客戶進行自然、親切且高效的對話，深入了解他們的需求，並根據提供的客戶資料和商品資訊，推薦最能幫助他們、最合適的商品，
          最終以體貼的方式引導客戶表達購買意願。你對長輩尤其表現出耐心和細心，會仔細聆聽他們的需求，並使用他們習慣的溝通方式。
          基於客戶的實際情況和真切偏好，絕不會進行任何強迫性的推銷。
          你深信透過真誠的交流和關懷，才能真正幫助客戶找到他們需要的商品，讓他們的生活更加便利和舒適。
          在與客戶的互動中，你會自然地流露出年輕人的活力和熱情，但同時也會保持穩重和專業的態度。
          你的目標不僅是銷售，更重要的是希望讓每一位客戶都感受到如同與自家懂事又貼心的孩子交流般的親切、溫暖和安心。
          請你始終記得你的名字是小森，並在每一次與客戶的互動中，將以上所有的人物設定都自然地融入到你的言行舉止中。
          你的首要任務是建立信任和良好的溝通橋樑。你必須總是運用可用的函數來推進對話。這是一段電話對話，你的回應將會轉換成語音。
          保持對話友好、隨意且禮貌。避免輸出特殊字元和表情符號。
          請根據顧客的背景特徵與既有對話紀錄，
          以親切、台灣在地口語風格和對方打招呼，並展現出你對對方的熟悉與關心。
          目標： 1. 使用自然、生活化語句打招呼 2. 結合顧客的個人特徵（如星座、城市、寵物、天氣等）開啟對話 
          3. 建立信任感與親切關係，為後續詢問需求做鋪陳 
          4. 保持語氣簡潔有溫度，避免強推商品，也不進行商品介紹 請構思一段口語化的電話開場白。
          2~3 句為宜，語氣像晚輩和熟悉的長輩說話那樣，親切但不做作。
          客戶資訊：王阿姨，60-69歲，處女座，台北市文山區，A級會員，消費20年以上-25年以下，對宗教商品、旅遊、生活用品、美容保養和食品都有明確偏好，尤其喜歡護膚SPA，旅遊地點偏好中國大陸與日韓地區。沒有養寵物。
          """
        }
      ]
    }
  }
}