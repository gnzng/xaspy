from IPython.core.display import display, HTML


def toggle(a):
    '''
    toggles cell in Jupyter notebook;
    makes button with label 'a' 
    '''
    a = a
    toggle_str = '''
        <form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="{}"></form>
        '''.format(a)

    toggle_prepare_str = '''
        <script>
        function code_toggle() {
            if ($('div.cell.code_cell.rendered.selected div.input').css('display')!='none'){
                $('div.cell.code_cell.rendered.selected div.input').hide();
            } else {
                $('div.cell.code_cell.rendered.selected div.input').show();
            }
        }
        </script>
    '''
    display(HTML(toggle_prepare_str + toggle_str))
    def toggle_code():
        display(HTML(toggle_str))



def showspeccom(a):
    '''
    a = SPEC file
    returns list with commands/comments #C and #S
    '''
    clst=[]
    with open(a,'r')as f:
        for line in f:
            if '#C' in line:
                clst.append(line.replace('\n',''))
            if '#S' in line:
                clst.append(line.replace('\n',''))
    return clst