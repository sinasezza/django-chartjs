from django.db import models



class CountryData(models.Model):
    country = models.CharField(max_length=100)
    population = models.PositiveSmallIntegerField()
    
    class Meta:
        verbose_name_plural = 'Countries Population Data'
        
    def __str__(self) -> str:
        return f"{self.country}: {self.population}"
    
