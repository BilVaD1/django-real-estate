from django.db import models
from django.utils.translation import gettext_lazy as _
from real_estate.settings.base import AUTH_USER_MODEL
from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Profile

class Rating(TimeStampedUUIDModel):
    
    class Range(models.IntegerChoices):
        RATING_1 = 1, _("Poor")
        RATING_2 = 2, _("Fair")
        RATING_3 = 3, _("Good")
        RATING_4 = 4, _("Very Good")
        RATING_5 = 5, _("Excellent")

    rater = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_("User providing the rating"), on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(Profile, verbose_name=_("Agent being rated"), related_name="agent_review", on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(verbose_name=_("Rating"), choices=Range.choices, help_text="1=Poor, 2=Fair, 3=Very Good, 5=Excellent", default=0)
    comment = models.TextField(verbose_name=_("Comment"))




    """
    Этот код указывает, что комбинация значений полей rater и agent должна быть уникальной в пределах этой модели. 
    Таким образом, это означает, что не может быть двух записей в этой модели с одинаковыми значениями rater и agent.

    В контексте оценок или рейтингов, это может использоваться, например, чтобы гарантировать, 
    что один пользователь (rater) не может оценить одного и того же агента (agent) более одного раза.
    """
    class Meta:
        unique_together = ["rater","agent"]

    def __str__(self) -> str:
        return f'{self.agent} rated at {self.rating}'