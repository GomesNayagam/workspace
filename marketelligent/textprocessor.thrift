enum DialogType {
    whQuestion = 1,
    ynQuestion = 2,
    Emphasis = 3,
    Statement = 4,
    Other = 5
}

struct DateTime {
    1: i16 Year,
    2: i16 Month,
    3: i16 Day,
    4: i16 Hour = 0,
    5: i16 Minute = 0
}

struct TimeValues {
    1: string sentence,
    2: list<string> dates,
    3: bool timeexpr_exists
}

service TextProcessor {
    DialogType infer_dialogtype(1:string DocID, 2:string DocText),
    TimeValues parse_time_expression(1:string sentence, 2:DateTime base_date),
    i16 infer_sentimentType(1:string DocText)
    i16 infer_subjectivity(1:string sentence)
}
