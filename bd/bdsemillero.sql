PGDMP     :    *                {            bisnesscontrol    15.3    15.3                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                        0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            !           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            "           1262    16467    bisnesscontrol    DATABASE     �   CREATE DATABASE bisnesscontrol WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';
    DROP DATABASE bisnesscontrol;
                postgres    false            �            1259    16468    cliente    TABLE     �   CREATE TABLE public.cliente (
    idcliente integer NOT NULL,
    nombrec character varying(100) NOT NULL,
    telefonoc numeric(15,2) NOT NULL,
    direccionc character varying(100)
);
    DROP TABLE public.cliente;
       public         heap    postgres    false            �            1259    16473    empleado    TABLE     �   CREATE TABLE public.empleado (
    idempleado integer NOT NULL,
    nombre character varying(100) NOT NULL,
    fechaingreso date NOT NULL,
    fechasalida date,
    cargo character varying(100) NOT NULL,
    correo character varying(100) NOT NULL
);
    DROP TABLE public.empleado;
       public         heap    postgres    false            �            1259    16483    producto    TABLE     �   CREATE TABLE public.producto (
    idproducto integer NOT NULL,
    nombreproducto character varying(100) NOT NULL,
    precio numeric(10,2) NOT NULL,
    codigo integer,
    idproveedores integer
);
    DROP TABLE public.producto;
       public         heap    postgres    false            �            1259    16478    proveedores    TABLE     �   CREATE TABLE public.proveedores (
    idproveedores integer NOT NULL,
    nombre character varying(100) NOT NULL,
    nit integer NOT NULL,
    direccion character varying(100),
    telefono integer
);
    DROP TABLE public.proveedores;
       public         heap    postgres    false            �            1259    16527    sesion    TABLE     j   CREATE TABLE public.sesion (
    "contraseña" character varying(100) NOT NULL,
    idempleado integer
);
    DROP TABLE public.sesion;
       public         heap    postgres    false            �            1259    16493    venta    TABLE     �   CREATE TABLE public.venta (
    idventa integer NOT NULL,
    horainicio timestamp with time zone,
    horafinal timestamp with time zone,
    idempleado integer,
    idcliente integer,
    idproducto integer
);
    DROP TABLE public.venta;
       public         heap    postgres    false                      0    16468    cliente 
   TABLE DATA           L   COPY public.cliente (idcliente, nombrec, telefonoc, direccionc) FROM stdin;
    public          postgres    false    214   �                 0    16473    empleado 
   TABLE DATA           `   COPY public.empleado (idempleado, nombre, fechaingreso, fechasalida, cargo, correo) FROM stdin;
    public          postgres    false    215   �                 0    16483    producto 
   TABLE DATA           ]   COPY public.producto (idproducto, nombreproducto, precio, codigo, idproveedores) FROM stdin;
    public          postgres    false    217                     0    16478    proveedores 
   TABLE DATA           V   COPY public.proveedores (idproveedores, nombre, nit, direccion, telefono) FROM stdin;
    public          postgres    false    216   6                  0    16527    sesion 
   TABLE DATA           ;   COPY public.sesion ("contraseña", idempleado) FROM stdin;
    public          postgres    false    219   S                  0    16493    venta 
   TABLE DATA           b   COPY public.venta (idventa, horainicio, horafinal, idempleado, idcliente, idproducto) FROM stdin;
    public          postgres    false    218   p        y           2606    16472    cliente cliente_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (idcliente);
 >   ALTER TABLE ONLY public.cliente DROP CONSTRAINT cliente_pkey;
       public            postgres    false    214            {           2606    16477    empleado empleado_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.empleado
    ADD CONSTRAINT empleado_pkey PRIMARY KEY (idempleado);
 @   ALTER TABLE ONLY public.empleado DROP CONSTRAINT empleado_pkey;
       public            postgres    false    215                       2606    16487    producto producto_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey PRIMARY KEY (idproducto);
 @   ALTER TABLE ONLY public.producto DROP CONSTRAINT producto_pkey;
       public            postgres    false    217            }           2606    16482    proveedores proveedores_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.proveedores
    ADD CONSTRAINT proveedores_pkey PRIMARY KEY (idproveedores);
 F   ALTER TABLE ONLY public.proveedores DROP CONSTRAINT proveedores_pkey;
       public            postgres    false    216            �           2606    16531    sesion sesion_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.sesion
    ADD CONSTRAINT sesion_pkey PRIMARY KEY ("contraseña");
 <   ALTER TABLE ONLY public.sesion DROP CONSTRAINT sesion_pkey;
       public            postgres    false    219            �           2606    16497    venta venta_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_pkey PRIMARY KEY (idventa);
 :   ALTER TABLE ONLY public.venta DROP CONSTRAINT venta_pkey;
       public            postgres    false    218            �           2606    16488 $   producto producto_idproveedores_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_idproveedores_fkey FOREIGN KEY (idproveedores) REFERENCES public.proveedores(idproveedores);
 N   ALTER TABLE ONLY public.producto DROP CONSTRAINT producto_idproveedores_fkey;
       public          postgres    false    217    3197    216            �           2606    16532    sesion sesion_idempleado_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.sesion
    ADD CONSTRAINT sesion_idempleado_fkey FOREIGN KEY (idempleado) REFERENCES public.empleado(idempleado);
 G   ALTER TABLE ONLY public.sesion DROP CONSTRAINT sesion_idempleado_fkey;
       public          postgres    false    215    219    3195            �           2606    16503    venta venta_idcliente_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_idcliente_fkey FOREIGN KEY (idcliente) REFERENCES public.cliente(idcliente);
 D   ALTER TABLE ONLY public.venta DROP CONSTRAINT venta_idcliente_fkey;
       public          postgres    false    214    218    3193            �           2606    16498    venta venta_idempleado_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_idempleado_fkey FOREIGN KEY (idempleado) REFERENCES public.empleado(idempleado);
 E   ALTER TABLE ONLY public.venta DROP CONSTRAINT venta_idempleado_fkey;
       public          postgres    false    3195    215    218            �           2606    16508    venta venta_idproducto_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_idproducto_fkey FOREIGN KEY (idproducto) REFERENCES public.producto(idproducto);
 E   ALTER TABLE ONLY public.venta DROP CONSTRAINT venta_idproducto_fkey;
       public          postgres    false    217    218    3199                  x������ � �            x������ � �            x������ � �            x������ � �            x������ � �            x������ � �     