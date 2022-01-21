from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from xraydb import xray_edges


def look_edges_db(element,edge='all'):
    '''
    uses xray_edges to return energies,fyield and jump ratio
    takes element, specific lines and group of lines
    '''
    try:
        edges = xray_edges(element)
    except:
        raise ValueError('cant find element {}, please try Co, Xe or F'.format(element))
    string = str()
    string = 'edges for {}: \n'.format(element)
    string = string + 'edge \t | energy \t | fyield \t | jump ratio\n'
    if edge == 'all':
        for n in edges.keys():
            string = string + str(n) + '\t | '+ str(edges[n][0])+' eV' + '\t | ' + str(edges[n][1])+ '\t | ' + str(edges[n][2]) + '\n'
    else:
        edge = edge.upper()
        try: 
            for n in edges.keys():
                if n.startswith(edge):
                    string = string + str(n) + '\t | '+ str(edges[n][0])+' eV' + '\t | ' + str(edges[n][1])+ '\t | ' + str(edges[n][2]) + '\n'          
        except:
            raise ValueError('cant find edge')
    return string 




def get_edge(update: Update, context: CallbackContext):
    """
    get edge of element
    prepares message for telegram bot
    """

    try:
        try: 
            element = str(context.args[0])
            edge = str(context.args[1])
            message = look_edges_db(element,edge)
        except:
            element = str(context.args[0])
            message = look_edges_db(element)     
    except:
        message = '''choose valid element, e.g. Co and edge: \n
                    Fe
                    Ni L 
                    Co L3
                    '''
    
    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='HTML')