from datetime import datetime
# Import HttpResponse module
from django.http import HttpResponse
from django.shortcuts import render
from .forms import GeneInputForm
from .gene_info_grabber import GeneInfoGrabber
from .models import *
import csv


def get_input(request):
    print('The request method is:', request.method)
    print('The POST data is:', request.POST)
    print('The GET data is:', request.GET)
    gene_names = None
    if request.method == 'POST':
        form = GeneInputForm(request.POST, request.FILES)
        upload_data = []
        if form.is_valid():
            input_textarea = form.cleaned_data['input_textarea']
            gene_list = input_textarea.split()
            # register user upload
            upload = Upload.objects.create(time_of_upload=datetime.now())
            for gene in gene_list:
                gene_info = GeneInfoGrabber(gene).processed_info
                upload_data.append(gene_info)
            upload.process_uploaddata(upload_data)
            # add gene transcripts and exons to database
    else:
        form = GeneInputForm()

    context = {'form': form, 'gene_names': gene_names, 'all_uploads': Upload.objects.all()}
    return render(request, 'app/index.html', context)


def Errorhandler500(request):
    data = {}
    return render(request, 'app/500.html', data)


def export_to_csv(request, *args, **kwargs):
    print(kwargs)

    upload_data = Upload.objects.get(id=kwargs['id'])
    gene_data = upload_data.uploaded_genes.all()
    transcript_data = Transcript.objects.all()
    exon_data = Exon.objects.filter(transcript_id__gene_id__in=gene_data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Results.csv"'
    writer = csv.writer(response)
    writer.writerow(['Time of Upload', 'User ID', 'Gene Symbol', 'Gene ID', 'Transcript ID', 'Coding',
                     'Strand', 'Chromosome', 'cdsStart', 'csdStop', 'exonStart', 'exonStop'])

    for exon in exon_data:
        writer.writerow([
            # time of upload
            upload_data.time_of_upload,
            # user id
            request.user,
            # gene symbol
            exon.transcript_id.gene_id.gene_symbol,
            # gene id
            exon.transcript_id.gene_id.gene_id,
            # transcript id
            exon.transcript_id.name,
            # coding
            exon.transcript_id.coding,
            # strand
            exon.transcript_id.strand,
            # chromosome
            exon.transcript_id.chromosome,
            # cdsStart
            exon.transcript_id.cdsStart,
            # cdsStop
            exon.transcript_id.cdsStop,
            # exonStart
            exon.exonStart,
            # exonStop
            exon.exonStop
        ])

    print(exon_data)
    return response
