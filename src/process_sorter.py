class ProcessSorter:
    # Sort processes by different criteria
    @staticmethod
    def sort_by_usage_time(list: list[dict], is_reverse: bool = True) -> list[dict]:
        # Sort processes by how long they've been running
        return sorted(list, key= lambda x: x.get('usage_time', 0), reverse=is_reverse)
    
    @staticmethod
    def sort_by_cpu_usage(list: list[dict], is_reverse: bool = True) -> list[dict]:
        # Sort processes by Cpu Usage
        return sorted(list, key= lambda x: x.get('cpu_usage', 0), reverse=is_reverse)

    @staticmethod
    def sort_by_memmory_usage(list: list[dict], is_reverse: bool = True) -> list[dict]:
        # Sort processes by Memmory usage
        return sorted(list, key= lambda x: x.get('memmory_info', {}).get('rss', 0), reverse=is_reverse) 
    
    @staticmethod
    def sort_by_name(list: list[dict], is_reverse: bool = True) -> list[dict]:
        # Sort processes by Name in alphabetical order
        return sorted(list, key= lambda x: x.get('name', '').lower(), reverse=is_reverse)