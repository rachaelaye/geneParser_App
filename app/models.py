from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction

class UserTracker(models.Model):
    """class for the user tracking data table."""
    assigned_userid = models.CharField(max_length=200)


class Gene(models.Model):
    """class for the gene data table."""
    gene_symbol = models.CharField(max_length=200)
    gene_id = models.CharField(max_length=200)
    chromosome = models.CharField(max_length=2)
    search_timestamp = models.DateTimeField()

    def __str__(self):
        return self.gene_symbol


class Upload(models.Model):
    """class for the upload data table."""
    time_of_upload = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_tracker_id = models.ForeignKey(UserTracker, on_delete=models.CASCADE, null=True)
    uploaded_genes = models.ManyToManyField(Gene)

    @transaction.atomic()
    def process_uploaddata(self, upload_data):
        print(upload_data)
        print(self.time_of_upload)

        for gene in upload_data:
            defaults = {
                'gene_symbol': gene['gene_symbol'],
                'chromosome': gene['chromosome'],
                'search_timestamp': gene['search_timestamp']}
            gene_model, created = Gene.objects.update_or_create(gene_id=gene['gene_id'], defaults=defaults)
            self.uploaded_genes.add(gene_model)
            self.save()

            print(self.uploaded_genes.all())

            for transcript in gene['transcripts']:
                print(gene_model)
                transcript_model, created = Transcript.objects.update_or_create(name=transcript['transcript_id'],
                                                                                coding=transcript['coding'],
                                                                                strand=gene['strand'],
                                                                                chromosome=gene['chromosome'],
                                                                                cdsStart=transcript['start'],
                                                                                cdsStop=transcript['stop'],
                                                                                gene_id=gene_model
                                                                                )
                print(transcript_model)

                for exon in transcript['exons']:
                    exon_model, created = Exon.objects.update_or_create(exonStart=exon['start'], exonStop=exon['end'],
                                                                        transcript_id=transcript_model)
                    print(exon_model)


class WmrglVersion(models.Model):
    """class for the WMRGL version data table."""
    UCSC_browser_update_date = models.DateTimeField()
    wmgl_version_number = models.IntegerField()


class Transcript(models.Model):
    """class for the transcript data table."""
    name = models.CharField(max_length=255)  # ensemble transcript id
    coding = models.CharField(max_length=3)
    strand = models.CharField(max_length=1)
    chromosome = models.CharField(max_length=255)
    cdsStart = models.IntegerField(null=True)
    cdsStop = models.IntegerField(null=True)
    wmrgl_version_id = models.ForeignKey(WmrglVersion, on_delete=models.CASCADE, null=True)
    gene_id = models.ForeignKey(Gene, on_delete=models.CASCADE, null=True)


class Exon(models.Model):
    """class for the exon data table."""
    exonStart = models.IntegerField()
    exonStop = models.IntegerField(null=True)
    transcript_id = models.ForeignKey(Transcript, on_delete=models.CASCADE, null=True)

