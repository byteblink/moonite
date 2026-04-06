class MerchantType(str, Enum):
    OFFICIAL = "official" # 自营
    FRANCHISE = "franchise" # 加盟
    SHARED = "shared" # 共享
    
    @property
    def label(self) -> str:
        return {
            MerchantType.OFFICIAL: "自营",
            MerchantType.FRANCHISE: "加盟",
            MerchantType.SHARED: "共享",
        }[self]