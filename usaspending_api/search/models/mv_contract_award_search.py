from usaspending_api.search.models.base_award_search import BaseAwardSearchModel


class ContractAwardSearchMatview(BaseAwardSearchModel):
    class Meta:
        managed = False
        db_table = "mv_contract_award_search"
