import dash_flask.plotlydash.cfg_geral  as cfg
import pandas as pd
import pyodbc


def conectar():
    SERVER_NAME = 'SOALV3SQLPROD,1438'
    DATABASE_NAME = 'dbEAcesso'

    return pyodbc.connect("""
            Driver={{SQL Server Native Client 11.0}};
            Server={0};
            Database={1};
            Trusted_Connection=yes;""".format(SERVER_NAME, DATABASE_NAME))


def q_chamados_mes():
    conn = conectar()
    sql_query = f"""
select
	c.id,
	CASE
		when GRUPOATRIBUIDO = 'OPERACAO - N1' then 'N1'
		WHEN GRUPOATRIBUIDO = 'SISTEMAS CORPORATIVOS' then 'N2'
	END AS GRUPOATRIBUIDO
	,CASE
		WHEN STATUSSLA = 'Within SLA' THEN 'NO SLA'
		WHEN STATUSSLA = 'Breached SLA' THEN 'FORA SLA'
	END AS STATUSSLA
	,CASE
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'NULL' THEN 'SEM CATEGORIA'
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'SISTEMAS' THEN 'STFCORP'
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'INFORME' THEN 'INF. RENDIMENTOS'
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'PESQUISA' THEN 'PESQ. CANDIDATO'
		ELSE UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1))
	END AS CATEGORIZACAO
	,CONCAT (SUBSTRING(atribuid, 1, CHARINDEX(' ', atribuid) - 1),' ',reverse (SUBSTRING(reverse(atribuid), 1, CHARINDEX(' ', reverse(atribuid)) - 1))) AS ANALISTA	
	,MES = MONTH(DTCRIACAO)
	,CASE
		WHEN MONTH(DTCRIACAO) = 1 THEN 'JAN'
		WHEN MONTH(DTCRIACAO) = 2 THEN 'FEV'
		WHEN MONTH(DTCRIACAO) = 3 THEN 'MAR'
		WHEN MONTH(DTCRIACAO) = 4 THEN 'ABR'
		WHEN MONTH(DTCRIACAO) = 5 THEN 'MAI'
		WHEN MONTH(DTCRIACAO) = 6 THEN 'JUN'
		WHEN MONTH(DTCRIACAO) = 7 THEN 'JUL'
		WHEN MONTH(DTCRIACAO) = 8 THEN 'AGO'
		WHEN MONTH(DTCRIACAO) = 9 THEN 'SET'
		WHEN MONTH(DTCRIACAO) = 10 THEN 'OUT'
		WHEN MONTH(DTCRIACAO) = 11 THEN 'NOV'
		WHEN MONTH(DTCRIACAO) = 12 THEN 'DEZ'
	END AS MESEXTENSO,
	CASE
		WHEN C.ID IN (SELECT ID FROM TBLCHAMADOSPESQUISA) THEN P.RESPOSTA
		ELSE NULL
	END AS RSERVICO,
	CASE
		WHEN C.ID IN (SELECT ID FROM TBLCHAMADOSPESQUISA) THEN P2.RESPOSTA
		ELSE NULL
	END AS RANALISTA,
	CASE
		WHEN C.ID IN (SELECT ID FROM TBLCHAMADOSPESQUISA) THEN 'SIM'
		ELSE 'NÃO'
	END AS RESPONDIDO

from TBLCHAMADOS c

left join DBEACESSO..TBLCHAMADOSPESQUISA p on c.ID = p.id AND p.PERGUNTA = 'Qual o nível de satisfação em relação a entrega dos serviços deste chamado?'
left join DBEACESSO..TBLCHAMADOSPESQUISA p2 on c.ID = p2.id AND p2.PERGUNTA = 'Qual é o nível de satisfação com a atuação do PO ou Analista?'

where 
	GRUPOATRIBUIDO in('SISTEMAS CORPORATIVOS','OPERACAO - N1')
	and c.CATEGORIZACAO not like'%causa%'
    and YEAR(DTCRIACAO)={cfg.ano} and MONTH(DTCRIACAO)>={cfg.mes_inicio} and MONTH(DTCRIACAO)<={cfg.mes_fim}
	and ATRIBUID NOT IN ('Thiago  De Campos Madeira', 'Izabel  Pereira De Jesus', 'Bruna  Ferreira De Paula', 'Ricardo  Januario Calabria', 'Niedja  Farias Neves Da Silva', 'Bruno  Santiago Primola De Souza')
	and c.STATUS IN ('CLOSED', 'Resolved-Validation')
	and STATUSSLA not in ('SLA Not Applied')         
ORDER BY MES ASC, GRUPOATRIBUIDO ASC
    """
    df = pd.read_sql(sql_query, conn)
    conn.close()

    return df


def q_reabertos():
    conn = conectar()
    sql_query = f"""
        select MONTH(dtabertura) as MES, 
		CASE
		WHEN MONTH(dtabertura) = 1 THEN 'JAN'
		WHEN MONTH(dtabertura) = 2 THEN 'FEV'
		WHEN MONTH(dtabertura) = 3 THEN 'MAR'
		WHEN MONTH(dtabertura) = 4 THEN 'ABR'
		WHEN MONTH(dtabertura) = 5 THEN 'MAI'
		WHEN MONTH(dtabertura) = 6 THEN 'JUN'
		WHEN MONTH(dtabertura) = 7 THEN 'JUL'
		WHEN MONTH(dtabertura) = 8 THEN 'AGO'
		WHEN MONTH(dtabertura) = 9 THEN 'SET'
		WHEN MONTH(dtabertura) = 10 THEN 'OUT'
		WHEN MONTH(dtabertura) = 11 THEN 'NOV'
		WHEN MONTH(dtabertura) = 12 THEN 'DEZ'
	END AS MESEXTENSO from TBLCHAMADOSREABERTOS 
		where ANALISTA NOT IN ('Thiago De Campos Madeira', 'Izabel Pereira De Jesus', 'Bruna Ferreira De Paula', 'Ricardo Januario Calabria', 'Niedja Farias Neves Da Silva')
        AND GRUPO NOT IN ('BACKOFFICE', 'FECHAMENTO')
        AND YEAR(DTABERTURA)=2022 and MONTH(DTABERTURA) >= {cfg.mes_inicio} and MONTH(DTABERTURA) <= {cfg.mes_fim}
    """

    df = pd.read_sql(sql_query, conn)
    conn.close()

    return df
