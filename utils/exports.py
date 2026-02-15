import json

def to_python_type(value):
    """Convert numpy / pandas types to native Python types"""
    if hasattr(value, "item"):
        return value.item()
    return value

def exports(summary, insights, summary_start, summary_end):
    clean_summary = {k: to_python_type(v) for k, v in summary.items()}
    clean_insights = {k: to_python_type(v) for k, v in insights.items()}
    

    return json.dumps(
        {
            "period": {
            "start_date": summary_start,
            "end_date": summary_end
        },
            "summary": clean_summary,
            "key_insights": clean_insights
        },
        indent=4
    )
