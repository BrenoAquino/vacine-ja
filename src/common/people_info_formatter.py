def people_info_formatter(people: dict) -> str:
    """
    Format the people informations to sentence.
    
    Parameters
    ----------
    people : dict
        People informations.
        
    Returns
    -------
    str
        Formatted sentence.
    """
    return people.nome + \
           ' nascido em ' + \
           people.data_nascimento + \
           ' tomará a ' + \
           people.dose + \
           ' no dia ' + \
           people.data_agendamento + \
           ' as ' + \
           people.hora_agendamento + \
           ' no ' + \
           people.ponto_atendimento