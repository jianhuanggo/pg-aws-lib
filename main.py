from _connect import _connect as _connect_
from typing import Dict


def test():
    _object_s3 = _connect_.get_object("awss3")
    print(_object_s3. list_buckets())
    # print(_object_s3.create_presigned_url("s3://pg-share-out-001/aws.jpg", expiration=604800))



def run():
    from task.analysis import analysis
    # analysis.find_similar_directory("adserver_metric_daily", "/Users/jian.huang/projects/dw/tubibricks/models")
    col_lst, groupby_lst, orderby_lst = analysis.get_table_info("/Users/jian.huang/anaconda3/envs/aws_lib/pg-aws-lib/task/801954")
    gen_group_list = analysis.generate_id_columns(col_lst, groupby_lst)
    sql_group_list = """
    {% set id_columns = ["ds", "platform", "country", "city", "subdivision", "dma", "language", "autoplay_on", "content_genres", "content_ratings", "content_type", "device_type", "revenue_vertical", "ramp_id_type", "identity_data_source", "ad_opportunity_reason", "opt_out", "is_coppa", "coppa_enabled", "Ad_break_position", "user_gender", "targeted_seq_pos", "device_deal", "remnant_status", "autoplay_idx", "tracking_mode", "app_mode", "Logged_status", "postal_code", "user_age"] %}
    """
    print(analysis.string_compare(gen_group_list, sql_group_list.strip()))


# def run1():
#     from _engine import _subprocess
#     command_line.run_command("ls -rlt", env_vars={
#         "MODEL_NAME": "adserver_metric_daily",
#         "MODEL_DIR": "adserver",
#         "TUBIBRICKS_HOME": "/Users/jian.huang/projects/dw/tubibricks"}
#     )

def run2(vars_dict: Dict):
    """

    Args:
        vars_dict:

    Returns:

    testing:

    #
    #
    # # from _engine._airflow import AirflowRunner
    # # commands = ["ls"]
    # # commands = ["ls", "echo xxx444", "ls -lrt"]
    # # shell_runner = AirflowRunner()
    # # execute_command(shell_runner, commands)
    #

    """

    # from _util import _util_directory as _util_directory_
    # print(_util_directory_.dirs_in_dir("/Users/jian.huang/anaconda3/envs/aws_lib/pg-aws-lib/task"))
    #
    # exit(0)
    # from task import task_completion
    #
    # task_completion._d123_process_sql_v1({})
    #
    # exit(0)

    # task_completion.get_task.get_task(800000)

    # from _management._meta import _inspect_module
    #
    # sql_file = _inspect_module.load_module_from_path("/Users/jian.huang/anaconda3/envs/aws_lib/pg-aws-lib/task/800000/jian_poc_model.py", "test")
    # print(sql_file.SQL)
    #
    # exit(0)


    from _engine._subprocess import ShellRunner
    from _engine._command_protocol import execute_command_from_dag

    from _pattern_template.template_v1 import model_history_load_template
    from _engine import _process_flow

    t_task = _process_flow.process_template(model_history_load_template)
    shell_runner = ShellRunner()
    execute_command_from_dag(shell_runner, t_task.tasks)
























    # filtered_vars = {name: value for name, value in locals().items() if name.startswith()}



def run_search():
    from _search import _semantic_search_faiss
    ss = _semantic_search_faiss.SemanticSearchFaiss("error_bank")

    _error_msg = {
        "process_name": "_subprocess",
        "error_type": "normal",
        "recovery_type": "normal",
        "recovery_method": ""
    }




    error_list = ["ValueError: not enough values to unpack (expected 2, got 1)",
                  "Error occurred: fatal: not a git repository (or any of the parent directories): .git",
                  "Error in 3 validation errors for DictValiatorModelAllString",
                  "Error occurred: error: pathspec 'jian_dbt_poc' did not match any file(s) known to git"
                  ]

    # for error in error_list:
    #     ss.add_index(error, _error_msg)

    # ss.add_index("this is a test")
    # # print(ss.search("is there a test there"))

    result = ss.search("ValueError: not enough values to unpack", k=3, threshold=10)
    print(result)


    exit(0)






    # class SemanticSearchFaiss:
    #     def __init__(self):
    #         self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    #
    #     def encode_message(self, message: str):
    #         embeddings = self.model.encode(message)
    #         embedding_shape = embeddings.shape
    #         print(embedding_shape)
    print(ss.load_index("/Users/jian.huang/anaconda3/envs/aws_lib/pg-aws-lib/search_index.json"))

"""
"""
def run10(search_string: str,
          replace_string: str):


    border_view_buffer = 20
    str_len = len(search_string)
    from _util import _util_file
    for each_file in _util_file.files_in_dir(
            "/Users/jian.huang/projects/dw/tubibricks/src/adserver_metric_daily/models/adserver"):
        print(each_file)
        notebook_file_str = _util_file.identity_load_file(each_file)

        index = notebook_file_str.find(search_string)
        if index <= 0:
            print("search string is not found in this file {each_file}")

        if replace_string:
            print(
                f"before the change!!! {notebook_file_str[index - border_view_buffer: index + str_len + border_view_buffer]}")
            notebook_file_str = notebook_file_str.replace(search_string, replace_string)
            _util_file.identity_write_file(each_file, notebook_file_str)
            notebook_file_str = _util_file.identity_load_file(each_file)

            print(
                f"after the change {notebook_file_str[index - border_view_buffer: index + str_len + border_view_buffer]}")




# def run_redshift():
#     from

def run_test1():

    directive_object = _connect_.get_directive("image_to_text")
    directive_object.run(**{"filepath": "/Users/jian.huang/Downloads/test.png"})
    # class DirectiveImage_to_text(metaclass=_meta_.MetaDirective):
    #     def __init__(self, config: _config_.ConfigSingleton = None, logger: Log = None):
    #         self._config = config if config else _config_.ConfigSingleton()
    #
    #     @_common_.exception_handler
    #     def run(self, *arg, **kwargs) -> str:
    #         return self._implementation_trocr(kwargs.get("filepath"))

def latest_template():
    from _engine._subprocess import ShellRunner
    from _engine._command_protocol import execute_command_from_dag

    from _pattern_template._process_template import _process_template

    # t_task = _process_template.process_template("/Users/jian.huang/anaconda3/envs/aws_lib/pg-aws-lib/_pattern_template/tubibricks_deployment_only.yaml", "config_dev")
    t_task = _process_template.process_template("config_prod", "/Users/jian.huang/anaconda3/envs/aws_lib/pg-aws-lib/_pattern_template/tubibricks_history_load_template.yaml", )

    shell_runner = ShellRunner()
    execute_command_from_dag(shell_runner, t_task.tasks)

if __name__ == '__main__':
    latest_template()
    exit(0)
    run_test1()
    exit(0)

    # run10("merge into `hive_metastore`.`tubidw`.`adserver_metric_daily`",
    #       "merge into `hive_metastore`.`tubidw_dev`.`adserver_metric_daily`")
    # exit(0)
    # run_search()
    # exit(0)


    run2({})
    exit(0)
    run1()
    exit(0)
    test()
