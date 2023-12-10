from config import RESOURCE_DIR, PCMIDS_FILE_PATH, INPUT_DIRfrom src.extraction_handler import ExtractionHandlerfrom multiprocessing import Process# noinspection SpellCheckingInspectionclass PcmManager:    pcmids: list[str] = []    handlers: list[ExtractionHandler] = []    @staticmethod    def _read_and_extract_list():        with open(PCMIDS_FILE_PATH, 'r') as file:            content = file.read()            elements = content.strip("[]").split(',')            elements = [element.strip().strip("'") for element in elements]            return elements    def __init__(self):        self.pcmids = self._read_and_extract_list()        #self.pcmids = ["PMC493283", "PMC497048", "PMC503396"]        self.handlers = [ExtractionHandler(), ExtractionHandler(), ExtractionHandler()]    def _extract_in_range_with_worker(self, worker_index, start, end):        for i in range(start, end):            _filename = self.pcmids[i]            self.handlers[worker_index].filename = _filename            _filename += ".xml"            try:                file = open(INPUT_DIR / _filename, 'r', encoding='utf-8')                self.handlers[worker_index].current_file = file                self.handlers[worker_index].extract_data_and_save_json_file()            except FileNotFoundError as e:                print(e)    def begin_parallel_extraction(self):        end = len(self.pcmids)        first_stop = end // 3        second_stop = 2 * first_stop        third_stop = end  # Ensure it covers the rest of the list        processes = [            Process(target=self._extract_in_range_with_worker, args=(0, 0, first_stop)),            Process(target=self._extract_in_range_with_worker, args=(1, first_stop, second_stop)),            Process(target=self._extract_in_range_with_worker, args=(2, second_stop, third_stop))        ]        for p in processes:            p.start()        # Wait for all processes to finish        for p in processes:            p.join()