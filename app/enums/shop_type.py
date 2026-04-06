class ShopType(str, Enum):
#    TEA_ROOM = "tea_room"  # 茶室
#    MAHJONG = "mahjong"  # 棋牌
#    BILLIARDS = "billiards"  # 桌球
#    KTV = "ktv"  # KTV
#    HOTEL = "hotel"  # 酒店
#    RESTAURANT = "restaurant"  # 餐厅
#    BBQ = "bbq"  # 烧烤
#    BATHHOUSE = "bathhouse"  # 浴场
#    PARTY = "party"  # 轰趴
   
    
    @property
    def label(self) -> str:
        return {
           
        }[self]