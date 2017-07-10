from django.db.models import F, Sum

from usaspending_api.awards.models import Transaction
from usaspending_api.awards.serializers import AwardTypeAwardSpendingSerializer
from usaspending_api.common.exceptions import InvalidParameterException
from usaspending_api.common.helpers import check_valid_toptier_agency
from usaspending_api.common.views import DetailViewSet
from usaspending_api.references.models import Agency


class AwardTypeAwardSpendingViewSet(DetailViewSet):
    """Return all award spending by award type for a given fiscal year and agency id"""

    serializer_class = AwardTypeAwardSpendingSerializer

    def get_queryset(self):
        # retrieve post request payload
        json_request = self.request.query_params

        # retrieve fiscal_year & awarding_agency_id from request
        fiscal_year = json_request.get('fiscal_year', None)
        awarding_agency_id = json_request.get('awarding_agency_id', None)

        # required query parameters were not provided
        if not (fiscal_year and awarding_agency_id):
            raise InvalidParameterException(
                'Missing one or more required query parameters: fiscal_year, awarding_agency_id'
            )

        if not check_valid_toptier_agency(awarding_agency_id):
            raise InvalidParameterException('Awarding Agency ID provided must correspond to a toptier agency')

        # change user provided PK (awarding_agency_id) to toptier_agency_id,
        # filter and include all subtier_agency_id(s).
        top_tier_agency_id = Agency.objects.filter(id=awarding_agency_id).first().toptier_agency_id
        queryset = Transaction.objects.all()
        # Filter based on fiscal year and agency id
        queryset = queryset.filter(
            fiscal_year=fiscal_year,
            awarding_agency__toptier_agency=top_tier_agency_id
        )
        # alias awards.category to be award_type
        queryset = queryset.annotate(
            award_type=F('award__category'),
            toptier_agency=F('awarding_agency__toptier_agency__name'),
            subtier_agency=F('awarding_agency__subtier_agency__name')
        )
        # sum obligations for each category type
        queryset = queryset.values('award_type', 'toptier_agency', 'subtier_agency').annotate(
            obligated_amount=Sum('federal_action_obligation')
        ).order_by('-obligated_amount')

        return queryset
