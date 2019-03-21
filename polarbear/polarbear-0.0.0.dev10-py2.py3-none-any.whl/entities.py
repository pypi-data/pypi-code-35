import pandas as pd
from savReaderWriter import SavWriter
from warnings import warn


class Mapping(object):

    def __init__(self, study_id, info=None):
        self.study_id = study_id

        if info is None:
            self.info = pd.DataFrame(
                columns=['question_id', 'database_question_id',
                         'exists_in_database', 'full_text', 'type_of_response',
                         'type_of_scale', 'scale_exists_in_database',
                         'scale_id', 'scale_name', 'display_text',
                         'category', 'subcategory', 'topic', 'subtopic'],
                data=[['id_in_study', None, None,
                       None, None, None, None, None, None,
                       None, None, None, None, None]])

        else:
            assert isinstance(info, pd.DataFrame), (
                "info argument should be a pandas DataFrame")
            assert "question_id" in info.columns, (
                "info should contain question_id column")
            assert "database_question_id" in info.columns, (
                "info should contain database_question_id column")
            assert "exists_in_database" in info.columns, (
                "info should contain exists_in_database column")
            assert "full_text" in info.columns, (
                "info should contain full_text column")
            assert "type_of_response" in info.columns, (
                "info should contain type_of_response column")
            assert "type_of_scale" in info.columns, (
                "info should contain type_of_scale column")
            assert "scale_exists_in_database" in info.columns, (
                "info should contain scale_exists_in_database column")
            assert "scale_id" in info.columns, (
                "info should contain scale_id column")
            assert "scale_name" in info.columns, (
                "info should contain scale_name column")
            assert "display_text" in info.columns, (
                "info should contain display_text column")
            assert "category" in info.columns, (
                "info should contain category column")
            assert "subcategory" in info.columns, (
                "info should contain subcategory column")
            assert "topic" in info.columns, (
                "info should contain topic column")
            assert "subtopic" in info.columns, (
                "info should contain subtopic column")
            assert "id_in_study" in list(info.question_id), (
                "question_id column in mapping should contain row for id_in_study")
            self.info = info

    def check_schema_conversion_readiness(self):
        assert isinstance(self.info, pd.DataFrame), (
            "info should be a pandas DataFrame")
        assert "question_id" in self.info.columns, (
            "info should contain question_id column")
        assert "database_question_id" in self.info.columns, (
            "info should contain database_question_id column")
        assert "exists_in_database" in self.info.columns, (
            "info should contain exists_in_database column")
        assert "full_text" in self.info.columns, (
            "info should contain full_text column")
        assert "type_of_response" in self.info.columns, (
            "info should contain type_of_response column")
        assert "type_of_scale" in self.info.columns, (
            "info should contain type_of_scale column")
        assert "scale_exists_in_database" in self.info.columns, (
            "info should contain scale_exists_in_database column")
        assert "scale_id" in self.info.columns, (
            "info should contain scale_id column")
        assert "scale_name" in self.info.columns, (
            "info should contain scale_name column")
        assert "display_text" in self.info.columns, (
            "info should contain display_text column")
        assert "category" in self.info.columns, (
            "info should contain category column")
        assert "subcategory" in self.info.columns, (
            "info should contain subcategory column")
        assert "topic" in self.info.columns, (
            "info should contain topic column")
        assert "subtopic" in self.info.columns, (
            "info should contain subtopic column")


class Dataset(object):

    def __init__(self, data, codebook=None, question_metadata=None):

        assert isinstance(data, pd.DataFrame), (
            "data argument should be a pandas DataFrame")
        self.data = data.apply(
            lambda x: x.astype(float, errors='ignore'), axis=1)

        if codebook is None:
            self.codebook = pd.DataFrame(columns=['question_id', 'value_code',
                                         'full_label', 'display_label'],
                                         dtype=float)
        else:
            assert isinstance(codebook, pd.DataFrame), (
                "codebook argument should be a pandas DataFrame")
            assert "question_id" in codebook.columns, (
                "codebook should contain question_id column")
            assert "value_code" in codebook.columns, (
                "codebook should contain value_code column")
            assert "full_label" in codebook.columns, (
                "codebook should contain full_label column")
            self.codebook = codebook
            self.codebook.value_code = self.codebook.value_code.astype(float)

        if question_metadata is None:
            m = pd.DataFrame(
                columns=['question_id', 'full_text', 'display_text',
                         'category', 'subcategory', 'topic', 'subtopic',
                         'type_of_response',
                         'scale_id', 'scale_name', 'type_of_scale'],
                dtype=float
            )
            m.question_id = data.columns
            self.question_metadata = m
        else:
            assert isinstance(question_metadata, pd.DataFrame), (
                "question_metadata argument should be a pandas DataFrame")
            assert "question_id" in question_metadata.columns, (
                "question_metadata should contain question_id column")
            self.question_metadata = question_metadata

    def add_id_in_study(self):
        self.data.insert(loc=0, column="id_in_study",
                         value=range(1, len(self.data) + 1))
        return self

    def add_value_code_to_codebook(self, questions, value,
                                   full_label, display_label):
        df = pd.DataFrame({'question_id': questions,
                           'value_code': value,
                           'full_label': full_label,
                           'display_label': display_label})
        self.codebook = self.codebook.append(df, ignore_index=True)
        return self

    def recode(self, to_recode, recoded_name, value_mapping,
               value_full_labels=None, value_display_labels=None):
        self.data[recoded_name] = self.data[to_recode].replace(value_mapping)

        d = [[recoded_name, x] for x in value_mapping.values()]
        codebook_to_append = pd.DataFrame(
            columns=['question_id', 'value_code'],
            data=d
        )
        if value_full_labels:
            codebook_to_append['full_label'] =\
                codebook_to_append['value_code'].replace(value_full_labels)
        if value_display_labels:
            codebook_to_append['display_label'] =\
                codebook_to_append['value_code'].replace(value_display_labels)

        self.codebook = self.codebook\
            .append(codebook_to_append)\
            .reset_index(drop=True)

        self.question_metadata = self.question_metadata\
            .append(pd.DataFrame([[recoded_name]], columns=['question_id']),
                    sort=False)\
            .reset_index(drop=True)

        return self

    def to_csv(self, filepath, codebook_path=None,
               question_metadata_path=None, encoding='utf-8', *args, **kwargs):
        self.data.to_csv(filepath, index=False, encoding=encoding,
                         *args, **kwargs)

        if codebook_path is None:
            codebook_path = filepath.replace('.csv', '_codebook.csv')
        else:
            codebook_path = codebook_path
        self.codebook.to_csv(codebook_path, index=False, encoding=encoding,
                             *args, **kwargs)

        if question_metadata_path is None:
            question_metadata_path = filepath.replace(
                '.csv', '_question_metadata.csv')
        else:
            question_metadata_path = question_metadata_path
        self.question_metadata.to_csv(question_metadata_path, index=False,
                                      encoding=encoding, *args, **kwargs)

    def to_excel(self, filepath, codebook_path=None,
                 question_metadata_path=None, encoding='utf-8',
                 *args, **kwargs):
        self.data.to_excel(filepath, index=False, encoding=encoding,
                           *args, **kwargs)

        if codebook_path is None:
            codebook_path = filepath.replace('.xlsx', '_codebook.xlsx')
        else:
            codebook_path = codebook_path
        self.codebook.to_excel(codebook_path, index=False, encoding=encoding,
                               *args, **kwargs)

        if question_metadata_path is None:
            question_metadata_path = filepath.replace(
                '.xlsx', '_question_metadata.xlsx')
        else:
            question_metadata_path = question_metadata_path
        self.question_metadata.to_excel(question_metadata_path, index=False,
                                        encoding=encoding, *args, **kwargs)

    def to_spss(self, filepath, *args, **kwargs):
        columns = self.question_metadata.question_id
        var_names = list(columns)
        var_types = {
            c: (0 if pd.api.types.is_numeric_dtype(self.data[c]) else
                int(self.data[c].str.len().max()))
            for c in columns}

        var_labels = dict(zip(self.question_metadata.question_id,
                              self.question_metadata.full_text))

        value_labels = ([{question_id: {d['value_code']: d['full_label'] for d
                        in self.codebook[self.codebook.question_id ==
                                         question_id].to_dict(
                            orient='records')}} for question_id in
                        self.codebook.question_id.unique()])
        value_labels = {k: v for d in value_labels for k, v in d.items()}

        records = self.data

        with SavWriter(filepath, var_names, var_types,
                       value_labels, var_labels, ioUtf8=True,
                       *args, **kwargs) as writer:
            for record in records.values:
                writer.writerow(record)

    def check_schema_conversion_readiness(self):
        assert isinstance(self.question_metadata, pd.DataFrame), (
            "question_metadata should be a pandas DataFrame")
        assert "question_id" in self.question_metadata.columns, (
            "question_metadata should contain question_id column")
        assert "full_text" in self.question_metadata.columns, (
            "question_metadata should contain full_text column")
        assert "display_text" in self.question_metadata.columns, (
            "question_metadata should contain display_text column")
        assert "category" in self.question_metadata.columns, (
            "question_metadata should contain category column")
        assert "subcategory" in self.question_metadata.columns, (
            "question_metadata should contain subcategory column")
        assert "topic" in self.question_metadata.columns, (
            "question_metadata should contain topic column")
        assert "subtopic" in self.question_metadata.columns, (
            "question_metadata should contain subtopic column")
        assert "type_of_response" in self.question_metadata.columns, (
            "question_metadata should contain type_of_response column")
        assert "scale_id" in self.question_metadata.columns, (
            "question_metadata should contain scale_id column")
        assert "scale_name" in self.question_metadata.columns, (
            "question_metadata should contain scale_name column")
        assert "type_of_scale" in self.question_metadata.columns, (
            "question_metadata should contain type_of_scale column")

        assert isinstance(self.data, pd.DataFrame), (
            "data should be a pandas DataFrame")
        assert "id_in_study" in self.data.columns, (
            "data should contain id_in_study column")

        assert isinstance(self.codebook, pd.DataFrame), (
            "codebook should be a pandas DataFrame")
        assert "question_id" in self.codebook.columns, (
            "codebook should contain question_id column")
        assert "value_code" in self.codebook.columns, (
            "codebook should contain value_code column")
        assert "full_label" in self.codebook.columns, (
            "codebook should contain full_label column")
        assert "display_label" in self.codebook.columns, (
            "codebook should contain display_label column")

    def to_schema(self, study):
        studies = pd.DataFrame(
            columns=['study_id', 'study_name', 'start_date', 'end_date'],
            data=[[study.study_id, study.study_name,
                   study.start_date, study.end_date]])
        studies_questions = pd.DataFrame({
            'study_id': study.study_id,
            'question_id': self.data.columns.values
        })
        respondents = pd.DataFrame(
            {'id_in_survey': self.data.index.values,
             'respondent_id': self.data.index.values})
        studies_respondents = pd.DataFrame({
            'study_id': study.study_id,
            'respondent_id': self.data.index.values
        })
        responses = pd.melt(self.data.reset_index(), id_vars='index',
                            var_name='question_id')
        responses.rename(columns={'index': 'respondent_id'}, inplace=True)
        responses['question_value_id'] = (
            responses["question_id"] + "_" +
            responses["value"].astype(int).astype(str))
        responses = responses[['respondent_id', 'question_value_id']]
        responses['study_id'] = study.study_id

        schema = Schema(
            studies, studies_questions, respondents,
            studies_respondents, responses)

        return schema


class Schema(object):

    def __init__(self, studies, question_orders, questions, scales,
                 response_choices, closed_ended_responses,
                 open_ended_responses):

        assert isinstance(studies, pd.DataFrame), (
            "studies argument should be a pandas DataFrame")
        assert "study_id" in studies.columns, (
            "studies should contain study_id column")
        assert "study_name" in studies.columns, (
            "studies should contain study_name column")
        assert "start_date" in studies.columns, (
            "studies should contain start_date column")
        assert "end_date" in studies.columns, (
            "studies should contain end_date column")
        self.studies = studies

        assert isinstance(question_orders, pd.DataFrame), (
            "question_orders argument should be a pandas DataFrame")
        assert "study_id" in question_orders.columns, (
            "question_orders should contain study_id column")
        assert "question_id" in question_orders.columns, (
            "question_orders should contain question_id column")
        assert "order" in question_orders.columns, (
            "question_orders should contain order column")
        self.question_orders = question_orders

        assert isinstance(questions, pd.DataFrame), (
            "questions argument should be a pandas DataFrame")
        assert "question_id" in questions.columns, (
            "questions should contain question_id column")
        assert "full_text" in questions.columns, (
            "questions should contain full_text column")
        assert "display_text" in questions.columns, (
            "questions should contain display_text column")
        assert "category" in questions.columns, (
            "questions should contain category column")
        assert "subcategory" in questions.columns, (
            "questions should contain subcategory column")
        assert "topic" in questions.columns, (
            "questions should contain topic column")
        assert "subtopic" in questions.columns, (
            "questions should contain subtopic column")
        assert "type_of_response" in questions.columns, (
            "questions should contain type_of_response column")
        assert "scale_id" in questions.columns, (
            "questions should contain scale_id column")
        self.questions = questions

        assert isinstance(scales, pd.DataFrame), (
            "scales argument should be a pandas DataFrame")
        assert "scale_id" in scales.columns, (
            "scales should contain scale_id column")
        assert "scale_name" in scales.columns, (
            "scales should contain scale_name column")
        assert "type_of_scale" in scales.columns, (
            "scales should contain type_of_scale column")
        self.scales = scales

        assert isinstance(response_choices, pd.DataFrame), (
            "response_choices argument should be a pandas DataFrame")
        assert "response_choice_id" in response_choices.columns, (
            "response_choices should contain response_choice_id column")
        assert "question_id" in response_choices.columns, (
            "response_choices should contain question_id column")
        assert "scale_id" in response_choices.columns, (
            "response_choices should contain scale_id column")
        assert "full_label" in response_choices.columns, (
            "response_choices should contain full_label column")
        assert "display_label" in response_choices.columns, (
            "response_choices should contain display_label column")
        assert "value" in response_choices.columns, (
            "response_choices should contain value column")
        self.response_choices = response_choices

        assert isinstance(closed_ended_responses, pd.DataFrame), (
            "closed_ended_responses argument should be a pandas DataFrame")
        assert "study_id" in closed_ended_responses.columns, (
            "closed_ended_responses should contain study_id column")
        assert "question_id" in closed_ended_responses.columns, (
            "closed_ended_responses should contain question_id column")
        assert "respondent_id" in closed_ended_responses.columns, (
            "closed_ended_responses should contain respondent_id column")
        assert "value" in closed_ended_responses.columns, (
            "closed_ended_responses should contain value column")
        self.closed_ended_responses = closed_ended_responses

        assert isinstance(open_ended_responses, pd.DataFrame), (
            "open_ended_responses argument should be a pandas DataFrame")
        assert "study_id" in open_ended_responses.columns, (
            "open_ended_responses should contain study_id column")
        assert "question_id" in open_ended_responses.columns, (
            "open_ended_responses should contain question_id column")
        assert "respondent_id" in open_ended_responses.columns, (
            "open_ended_responses should contain respondent_id column")
        assert "text_response" in open_ended_responses.columns, (
            "open_ended_responses should contain text_response column")
        self.open_ended_responses = open_ended_responses

    def to_csv(self, studies_filepath,
               question_orders_filepath,
               questions_filepath,
               scales_filepath,
               response_choices_filepath,
               closed_ended_responses_filepath,
               open_ended_responses_filepath,
               encoding='utf-8', *args, **kwargs):
        self.studies.to_csv(
            studies_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.question_orders.to_csv(
            question_orders_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.questions.to_csv(
            questions_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.scales.to_csv(
            scales_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.response_choices.to_csv(
            response_choices_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.closed_ended_responses.to_csv(
            closed_ended_responses_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.open_ended_responses.to_csv(
            open_ended_responses_filepath, index=False, encoding=encoding,
            *args, **kwargs)

    def to_excel(self, studies_filepath,
                 question_orders_filepath,
                 questions_filepath,
                 scales_filepath,
                 response_choices_filepath,
                 closed_ended_responses_filepath,
                 open_ended_responses_filepath,
                 encoding='utf-8', *args, **kwargs):
        self.studies.to_excel(
            studies_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.question_orders.to_excel(
            question_orders_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.questions.to_excel(
            questions_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.scales.to_excel(
            scales_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.response_choices.to_excel(
            response_choices_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.closed_ended_responses.to_excel(
            closed_ended_responses_filepath, index=False, encoding=encoding,
            *args, **kwargs)
        self.open_ended_responses.to_excel(
            open_ended_responses_filepath, index=False, encoding=encoding,
            *args, **kwargs)

    def to_sql(self, connection, *args, **kwargs):
        self.studies.to_sql(
            'studies', connection, *args, **kwargs)
        self.question_orders.to_sql(
            'question_orders', connection, *args, **kwargs)
        self.questions.to_sql(
            'questions', connection, *args, **kwargs)
        self.scales.to_sql(
            'scales', connection, *args, **kwargs)
        self.response_choices.to_sql(
            'response_choices', connection, *args, **kwargs)
        self.closed_ended_responses.to_sql(
            'closed_ended_responses', connection, *args, **kwargs)
        self.open_ended_responses.to_sql(
            'open_ended_responses', connection, *args, **kwargs)

    def study_id_order(self, study_id_order=None):
        if study_id_order:
            study_id_difference = (set(study_id_order) -
                                   set(self.studies['study_id']))
            if study_id_difference != set():
                warn("study_id %s is not in the studies table" %
                     (study_id_difference))

            study_id_difference = (
                set(self.studies['study_id']) - set(study_id_order))
            if study_id_difference != set():
                warn("study_id %s is in the studies table, but not provided in study_id_order"
                     % (study_id_difference))

            study_id_order = study_id_order
        else:
            study_id_order = self.studies.sort_values(
                'start_date', ascending=False).study_id.tolist()
        return study_id_order

    def study_id_order_sorter(self, study_id_order=None):
        study_id_order = self.study_id_order(study_id_order=study_id_order)
        return dict(zip(study_id_order, range(len(study_id_order))))

    def question_id_order(self, study_id_order=None, question_id_order=None):

        if question_id_order:
            question_id_difference = (
                set(question_id_order) - set(self.questions['question_id']))
            if question_id_difference != set():
                warn("question_id %s is not in the questions table.\
                     Will use default question_id_order instead." %
                     (question_id_difference))
                question_id_order = None
            else:

                question_id_difference = (set(
                    self.questions['question_id']) - set(question_id_order))
                if question_id_difference != set():
                    warn("question_id %s is in the questions table, but not provided in question_id_order.\
                         Will use default question_id_order instead."
                         % (question_id_difference))
                    question_id_order = None
            question_id_order = question_id_order
        else:
            study_id_order_sorter = self.study_id_order_sorter(
                study_id_order=study_id_order)

            _question_orders = self.question_orders.copy()
            _question_orders['study_id_order'] = _question_orders['study_id']\
                .map(study_id_order_sorter)
            question_id_order = _question_orders\
                .sort_values(['study_id_order', 'order'])\
                .drop_duplicates(subset=['question_id']).question_id.tolist()
        return question_id_order

    def question_id_order_sorter(self, study_id_order=None,
                                 question_id_order=None):
        if question_id_order:
            question_id_order = question_id_order
        else:
            question_id_order = self.question_id_order(
                study_id_order=study_id_order, question_id_order=None)
        return dict(zip(question_id_order, range(len(question_id_order))))

    def codebook_for_dataset(self, question_id_order_sorter=None):
        if question_id_order_sorter:
            question_id_order_sorter = question_id_order_sorter
        else:
            question_id_order_sorter = self.question_id_order_sorter()

        codebook = self\
            .response_choices[['question_id','value','full_label','display_label']]\
            .rename(columns={'value': 'value_code'})
        codebook['question_id_order'] = codebook['question_id']\
            .map(question_id_order_sorter)
        codebook = codebook.sort_values('question_id_order')\
                           .drop('question_id_order', axis=1)\
                           .reset_index(drop=True)
        return codebook

    def question_metadata_for_dataset(self, question_id_order_sorter=None):
        if question_id_order_sorter:
            question_id_order_sorter = question_id_order_sorter
        else:
            question_id_order_sorter = self.question_id_order_sorter()

        scales_info = self.scales[['scale_id', 'scale_name', 'type_of_scale']]
        question_metadata = self.questions[['question_id', 'full_text',
                                            'display_text', 'category',
                                            'subcategory', 'topic',
                                            'subtopic', 'type_of_response',
                                            'scale_id']]\
                                .merge(scales_info, how='left', on='scale_id')
        question_metadata['question_id_order'] = \
            question_metadata['question_id'].map(question_id_order_sorter)
        question_metadata = question_metadata\
            .sort_values('question_id_order')\
            .drop('question_id_order', axis=1)\
            .reset_index(drop=True)
        return question_metadata

    def data_for_dataset(self, study_id_order=None, question_id_order=None):
        study_id_order_sorter = self.study_id_order_sorter(
            study_id_order=study_id_order)

        pivoted_closed_ended_responses = self.closed_ended_responses\
            .pivot_table(
                values='value', index=['study_id', 'respondent_id'],
                columns='question_id')
        pivoted_open_ended_responses = self.open_ended_responses.pivot_table(
            values='text_response',
            index=['study_id', 'respondent_id'],
            columns='question_id',
            aggfunc=lambda x: x)

        data = pivoted_closed_ended_responses\
            .merge(pivoted_open_ended_responses,
                   how='outer', on=['study_id', 'respondent_id'])\
            .reset_index()
        data = data\
            .merge(self.studies[['study_id', 'start_date']],
                   how='left', on='study_id')\
            .rename(columns={'start_date': 'study_start_date'})
        data = data[['study_id', 'study_start_date', 'respondent_id'] +
                    self.question_id_order(
                        study_id_order=study_id_order,
                        question_id_order=question_id_order)]
        data['study_id_order'] = data['study_id'].map(study_id_order_sorter)
        data = data.sort_values('study_id_order')\
                   .drop('study_id_order', axis=1)\
                   .reset_index(drop=True)
        return data

    def to_dataset(self, study_id_order=None, question_id_order=None):
        study_id_order_for_dataset = self.study_id_order(
            study_id_order=study_id_order)
        question_id_order_for_dataset = self.question_id_order(
            study_id_order=study_id_order_for_dataset,
            question_id_order=question_id_order)
        question_id_order_sorter = self.question_id_order_sorter(
            study_id_order=study_id_order_for_dataset,
            question_id_order=question_id_order_for_dataset)

        data = self.data_for_dataset(
            study_id_order=study_id_order_for_dataset,
            question_id_order=question_id_order_for_dataset)
        codebook = self.codebook_for_dataset(
            question_id_order_sorter=question_id_order_sorter)
        question_metadata = self.question_metadata_for_dataset(
            question_id_order_sorter=question_id_order_sorter)

        ds = Dataset(data, codebook, question_metadata)
        return ds
