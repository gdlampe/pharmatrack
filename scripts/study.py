import io
import requests
import pandas as pd

from pharma_track.models import Drug, Study

def _study_scrap(drug):
    headers = [
        'rank',
        'nct_id',
        'title',
        'acronym',
        'status',
        'study_results',
        'conditions',
        'interventions',
        'outcome_measures',
        'sponsor',
        'gender',
        'age',
        'phase',
        'enrollment',
        'funded_by',
        'study_type',
        'study_design',
        'other_ids',
        'start_date',
        'primary_completion_date',
        'completion_date',
        'first_posted',
        'results_first_posted',
        'last_update_posted',
        'locations',
        'study_documents',
        'url'
    ]
    request_url = "https://clinicaltrials.gov/ct2/results/download_fields"
    params = {
        'down_count': 1000,
        'down_flds': 'all',
        'down_fmt': 'csv',
        'phase': 0,
        'flds': 'a',
        'flds': 'b',
        'flds': 'i',
        'flds': 'f',
        'flds': 'c',
        'flds': 'h',
        'flds': 'j',
        'flds': 'v',
        'flds': 'y',
    }

    if drug.indication:
        params['cond'] = drug.indication

    if drug.name:
        params['intr'] = drug.name

    if drug.phase:
        try:
            phase = int(drug.phase.split()[1]) - 1
        except Exception:
            pass
        else:
            params['phase'] = phase
    r = requests.get(request_url, params=params)
    df = pd.read_csv(io.StringIO(r.text), skiprows=1, names=headers)
    return df

def save_study(drug, data):
    if data.nct_id == 'nan':
        return
    study = drug.studies.filter(nct_id=data.nct_id).first()
    if not study:
        study = Study()

    study.drug = drug
    study.nct_id = data.nct_id
    study.title = data.title
    study.acronym = data.acronym
    study.status = data.status
    study.study_results = data.study_results
    study.interventions = data.interventions
    study.outcome_measures = data.outcome_measures
    study.sponsor = data.sponsor
    study.gender = data.gender
    study.age = data.age
    study.phase = data.phase
    study.funded_by = data.funded_by
    study.study_type = data.study_type
    study.study_design = data.study_design
    study.other_ids = data.other_ids
    study.start_date = data.start_date
    study.primary_completion_date = data.primary_completion_date
    study.completion_date = data.completion_date
    study.first_posted = data.first_posted
    study.results_first_posted = data.results_first_posted
    study.last_update_posted = data.last_update_posted
    study.locations = data.locations
    study.study_documents = data.study_documents
    study.url = data.url
    study.save()

    phase = drug.phase
    try:
        pno = study.phase.split()[-1]
        tp = 'Phase {}'.format(pno)
        if tp > phase:
            drug.phase = tp
            drug.version += 1
            drug.save()
    except Exception as e:
        pass

def run():
    drugs = Drug.objects.all()
    Study.objects.all().delete()
    counter = 0
    for drug in drugs:
        counter += 1
        print(counter)
        study_data = _study_scrap(drug)
        for data in study_data.itertuples():
            save_study(drug, data)
